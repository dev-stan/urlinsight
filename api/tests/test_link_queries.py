from app.db.models import Link
from app.services.links.queries import (
    create_unique_link,
    get_daily_clicks,
    get_daily_unique_visits,
    get_total_clicks,
    get_total_unique_visits,
)


class TestCreateUniqueLink:
    def test_creates_link(self, db):
        link = create_unique_link(db, "https://example.com")
        assert link.id is not None
        assert link.target_url == "https://example.com"
        assert len(link.short_code) == 6

    def test_persists_in_database(self, db):
        link = create_unique_link(db, "https://example.com")
        fetched = db.query(Link).filter(Link.id == link.id).first()
        assert fetched is not None
        assert fetched.short_code == link.short_code

    def test_unique_codes(self, db):
        codes = set()
        for _ in range(10):
            link = create_unique_link(db, "https://example.com")
            codes.add(link.short_code)
        assert len(codes) == 10


class TestGetTotalClicks:
    def test_zero_when_no_events(self, db, sample_link):
        assert get_total_clicks(db, sample_link.id) == 0

    def test_counts_events(self, db, sample_link_with_events):
        assert get_total_clicks(db, sample_link_with_events.id) == 3


class TestGetTotalUniqueVisits:
    def test_zero_when_no_visits(self, db, sample_link):
        assert get_total_unique_visits(db, sample_link.id) == 0

    def test_counts_unique_visits(self, db, sample_link_with_events):
        assert get_total_unique_visits(db, sample_link_with_events.id) == 2


class TestGetDailyClicks:
    def test_empty_when_no_events(self, db, sample_link):
        result = get_daily_clicks(db, sample_link.id)
        assert result == []

    def test_groups_by_date(self, db, sample_link_with_events):
        result = get_daily_clicks(db, sample_link_with_events.id)
        assert len(result) >= 1
        total = sum(row.clicks for row in result)
        assert total == 3


class TestGetDailyUniqueVisits:
    def test_empty_when_no_visits(self, db, sample_link):
        result = get_daily_unique_visits(db, sample_link.id)
        assert result == []

    def test_groups_by_date(self, db, sample_link_with_events):
        result = get_daily_unique_visits(db, sample_link_with_events.id)
        assert len(result) >= 1
        total = sum(row.unique_visitors for row in result)
        assert total == 2
