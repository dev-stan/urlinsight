from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_link_or_404
from app.db.database import get_db
from app.db.models import Link
from app.schemas.link import LinkCreate, LinkResponse
from app.services.links.normalizers import normalize_link_analytics
from app.services.links.queries import (
    create_unique_link,
    get_daily_clicks,
    get_daily_unique_visits,
    get_total_clicks,
    get_total_unique_visits,
)

router = APIRouter(prefix="/links", tags=["links"])


@router.post("", response_model=LinkResponse)
def create_link(link_in: LinkCreate, db: Session = Depends(get_db)):
    return create_unique_link(db, link_in.target_url)


@router.get("", response_model=list[LinkResponse])
def list_links(db: Session = Depends(get_db)):
    return db.query(Link).all()


@router.get("/{short_code}", response_model=LinkResponse)
def get_link(link: Link = Depends(get_link_or_404)):
    return link


@router.get("/{short_code}/analytics")
def link_analytics(db: Session = Depends(get_db), link: Link = Depends(get_link_or_404)):
    # fetch raw DB data
    total_clicks = get_total_clicks(db, link.id)
    total_unique_visits = get_total_unique_visits(db, link.id)
    daily_clicks = get_daily_clicks(db, link.id)
    daily_unique_visits = get_daily_unique_visits(db, link.id)

    # normalize for API response
    return normalize_link_analytics(link, total_clicks, total_unique_visits, daily_clicks, daily_unique_visits)
