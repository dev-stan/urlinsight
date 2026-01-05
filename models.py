from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base
from datetime import datetime, timezone

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    ip_hash = Column(String(64), nullable=True)
    user_agent = Column(String(512), nullable=True)
    referrer = Column(String(512), nullable=True)
    is_bot = Column(Integer, default=0)