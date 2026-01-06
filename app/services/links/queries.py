from sqlalchemy import Date, func
from app.db.models import ClickEvent, ClickEvent, Link, UniqueVisit
from app.services.links.utils import generate_short_code
from sqlalchemy.orm import Session


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

def get_total_clicks(db: Session, link_id: int) -> int:
    return db.query(func.count(ClickEvent.id)).filter(ClickEvent.link_id == link_id).scalar()

def get_total_unique_visits(db: Session, link_id: int) -> int:
    return db.query(func.count(UniqueVisit.id)).filter(UniqueVisit.link_id == link_id).scalar()

def get_daily_clicks(db: Session, link_id: int):
    return db.query(
        func.date(ClickEvent.created_at, type_=Date).label("date"),
        func.count(ClickEvent.id).label("clicks")
    ).filter(ClickEvent.link_id == link_id).group_by("date").all()

def get_daily_unique_visits(db: Session, link_id: int):
    return db.query(
        UniqueVisit.date,
        func.count(UniqueVisit.id).label("unique_visitors")
    ).filter(UniqueVisit.link_id == link_id).group_by(UniqueVisit.date).all()