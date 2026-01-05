# routers/links.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import LinkCreate, LinkResponse
from dependencies import get_link_or_404
from database import get_db
from services.links import create_unique_link
from models import Link

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
