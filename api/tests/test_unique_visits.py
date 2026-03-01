from datetime import date

from app.db.models import UniqueVisit
from app.services.unique_visits.queries import create_unique_visit


class TestCreateUniqueVisit:
    def test_new_visit_returns_true(self, db, sample_link):
        result = create_unique_visit(db, sample_link.id, "new_ip_hash")
        assert result is True

    def test_persists_in_database(self, db, sample_link):
        create_unique_visit(db, sample_link.id, "new_ip_hash")
        visit = db.query(UniqueVisit).filter(UniqueVisit.link_id == sample_link.id).first()
        assert visit is not None
        assert visit.ip_hash == "new_ip_hash"
        assert visit.date == date.today()

    def test_duplicate_same_day_returns_false(self, db, sample_link):
        first = create_unique_visit(db, sample_link.id, "same_hash")
        second = create_unique_visit(db, sample_link.id, "same_hash")
        assert first is True
        assert second is False

    def test_duplicate_does_not_create_extra_row(self, db, sample_link):
        create_unique_visit(db, sample_link.id, "dup_hash")
        create_unique_visit(db, sample_link.id, "dup_hash")
        count = db.query(UniqueVisit).filter(UniqueVisit.link_id == sample_link.id).count()
        assert count == 1

    def test_different_ips_same_day(self, db, sample_link):
        create_unique_visit(db, sample_link.id, "hash_a")
        create_unique_visit(db, sample_link.id, "hash_b")
        count = db.query(UniqueVisit).filter(UniqueVisit.link_id == sample_link.id).count()
        assert count == 2

    def test_same_ip_different_links(self, db, sample_link):
        from app.db.models import Link

        other_link = Link(short_code="xyz789", target_url="https://other.com")
        db.add(other_link)
        db.commit()
        db.refresh(other_link)

        create_unique_visit(db, sample_link.id, "shared_hash")
        create_unique_visit(db, other_link.id, "shared_hash")

        count = db.query(UniqueVisit).count()
        assert count == 2
