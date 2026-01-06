import random, string
from sqlalchemy.orm import Session
from app.db.models import Link
from sqlalchemy import Date, func
from app.db.models import ClickEvent, UniqueVisit
import datetime as dt


def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_unique_link(db: Session, target_url: str) -> Link:
    short_code = generate_short_code()

    # Ensure uniqueness (simple retry loop)
    while db.query(Link).filter(Link.short_code == short_code).first():
        short_code = generate_short_code()

    link = Link(short_code=short_code, target_url=target_url)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def get_link_analytics(db: Session, link_id: int, short_code: str, target_url: str):
    total_clicks = db.query(func.count(ClickEvent.id)).filter(ClickEvent.link_id == link_id).scalar()
    total_uniques = db.query(func.count(UniqueVisit.id)).filter(UniqueVisit.link_id == link_id).scalar()

    daily_clicks = db.query(
        func.date(ClickEvent.created_at, type_=Date).label("date"),
        func.count(ClickEvent.id).label("clicks")
    ).filter(ClickEvent.link_id == link_id).group_by("date").all()

    daily_uniques = db.query(
        UniqueVisit.date,
        func.count(UniqueVisit.id).label("unique_visitors")
    ).filter(UniqueVisit.link_id == link_id).group_by(UniqueVisit.date).all()

    # normalize everything to date objects
    clicks_by_date = {row.date: row.clicks for row in daily_clicks}
    uniques_by_date = {
        row.date if isinstance(row.date, dt.date) else dt.date.fromisoformat(row.date): row.unique_visitors
        for row in daily_uniques
    }

    all_dates = sorted(set(clicks_by_date.keys()) | set(uniques_by_date.keys()))

    daily = [
        {"date": d.isoformat(), "clicks": clicks_by_date.get(d, 0), "unique_visitors": uniques_by_date.get(d, 0)}
        for d in all_dates
    ]

    return {
        "short_code": short_code,
        "target_url": target_url,
        "totals": {"clicks": total_clicks, "unique_visitors": total_uniques},
        "daily": daily,
    }