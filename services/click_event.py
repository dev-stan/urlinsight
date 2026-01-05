from sqlalchemy.orm import Session
from fastapi import Request


def create_click_event(db: Session, link_id: int, ip_hash: str, user_agent: str, referrer: str):
    from models import ClickEvent

    click_event = ClickEvent(
        link_id=link_id,
        ip_hash=ip_hash,
        user_agent=user_agent,
        referrer=referrer,
        is_bot=0  # I'll add this soon(-ish)
    )
    db.add(click_event)
    db.commit()
    db.refresh(click_event)
    return click_event