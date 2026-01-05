from fastapi.params import Depends
from app.db.models import Link
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db

def get_link_or_404(short_code: str, db: Session = Depends(get_db)) -> Link:
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link