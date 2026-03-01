from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.auth import decode_access_token
from app.db.database import get_db
from app.db.models import Link, User
from app.services.users.queries import get_user_by_id


def get_link_or_404(short_code: str, db: Session = Depends(get_db)) -> Link:
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


def _extract_token(request: Request) -> str | None:
    auth = request.headers.get("authorization")
    if auth and auth.startswith("Bearer "):
        return auth[7:]
    return None


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = _extract_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    token = _extract_token(request)
    if not token:
        return None
    user_id = decode_access_token(token)
    if user_id is None:
        return None
    return get_user_by_id(db, user_id)
