
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from dependencies import get_link_or_404
from models import Link

router = APIRouter(prefix="/redirect", tags=["redirect"])

@router.get("/{short_code}", response_class=RedirectResponse)
def redirect_link(link: Link = Depends(get_link_or_404)):
    return link.target_url
