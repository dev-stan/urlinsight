from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.link import LinkCreate, LinkResponse
from app.api.deps import get_link_or_404
from app.db.database import get_db
from app.services.links import create_unique_link, get_link_analytics
from app.db.models import Link

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
def link_analytics(link = Depends(get_link_or_404), db: Session = Depends(get_db)):
    return get_link_analytics(db, link.id, link.short_code, link.target_url)