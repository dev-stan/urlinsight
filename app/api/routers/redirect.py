
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.api.deps import get_link_or_404
from app.db.models import Link
from app.services.click_event import create_click_event
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Request


router = APIRouter(prefix="/redirect", tags=["redirect"])

@router.get("/{short_code}", response_class=RedirectResponse)
def redirect_link(request: Request, link: Link = Depends(get_link_or_404), db: Session = Depends(get_db)):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    create_click_event(
        db=db,
        link_id=link.id,
        ip_hash=(ip),
        user_agent=user_agent,
        referrer=referrer
    )
    return link.target_url
