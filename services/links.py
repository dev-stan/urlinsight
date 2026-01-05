import random, string
from sqlalchemy.orm import Session
from models import Link

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_unique_link(db: Session, target_url: str) -> Link:
    short_code = generate_short_code()

    # Ensure uniqueness (simple retry loop)
    while db.query(Link).filter(Link.short_code == short_code).first():
        short_code = generate_short_code()

    link = Link(short_code=short_code, target_url=target_url)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link