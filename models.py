from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    target_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
