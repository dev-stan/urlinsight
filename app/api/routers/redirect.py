
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.api.deps import get_link_or_404
from app.db.models import Link
from app.services.click_event import create_click_event
from app.services.unique_visit import create_unique_visit
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Request
from app.core.security import hash_ip


router = APIRouter(prefix="/redirect", tags=["redirect"])

@router.get("/{short_code}", response_class=RedirectResponse)
def redirect_link(request: Request, link: Link = Depends(get_link_or_404), db: Session = Depends(get_db)):
    ip_hash = hash_ip(request.client.host)
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    create_click_event(
        db=db,
        link_id=link.id,
        ip_hash=ip_hash,
        user_agent=user_agent,
        referrer=referrer
    )

    create_unique_visit(
        db=db,
        link_id=link.id,
        ip_hash=(ip_hash)
    )

    return link.target_url
