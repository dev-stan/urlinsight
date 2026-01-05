from datetime import datetime, timezone, date
from sqlalchemy.exc import IntegrityError
from app.db.models import UniqueVisit

def create_unique_visit(db, link_id: int, ip_hash: str) -> bool:
    today: date = datetime.now(timezone.utc).date()

    unique_visit = UniqueVisit(
        link_id=link_id,
        ip_hash=ip_hash,
        date=today,
    )

    try:
        db.add(unique_visit)
        db.commit()
        return True # new unique
    except IntegrityError:
        db.rollback()
        return False # already counted today
