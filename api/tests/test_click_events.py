from app.db.models import ClickEvent
from app.services.click_events.queries import create_click_event


class TestCreateClickEvent:
    def test_creates_event(self, db, sample_link):
        event = create_click_event(
            db=db,
            link_id=sample_link.id,
            ip_hash="abcdef1234567890",
            user_agent="Mozilla/5.0",
            referrer="https://google.com",
        )
        assert event.id is not None
        assert event.link_id == sample_link.id
        assert event.ip_hash == "abcdef1234567890"
        assert event.user_agent == "Mozilla/5.0"
        assert event.referrer == "https://google.com"
        assert event.is_bot == 0

    def test_persists_in_database(self, db, sample_link):
        event = create_click_event(
            db=db,
            link_id=sample_link.id,
            ip_hash="hash",
            user_agent="agent",
            referrer="ref",
        )
        fetched = db.query(ClickEvent).filter(ClickEvent.id == event.id).first()
        assert fetched is not None

    def test_nullable_fields(self, db, sample_link):
        event = create_click_event(
            db=db,
            link_id=sample_link.id,
            ip_hash="hash",
            user_agent=None,
            referrer=None,
        )
        assert event.user_agent is None
        assert event.referrer is None

    def test_multiple_events_for_same_link(self, db, sample_link):
        for i in range(5):
            create_click_event(
                db=db,
                link_id=sample_link.id,
                ip_hash=f"hash_{i}",
                user_agent="agent",
                referrer=None,
            )
        count = db.query(ClickEvent).filter(ClickEvent.link_id == sample_link.id).count()
        assert count == 5
