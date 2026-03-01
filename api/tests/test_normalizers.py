import datetime as dt
from collections import namedtuple

from app.services.links.normalizers import normalize_link_analytics

DailyClick = namedtuple("DailyClick", ["date", "clicks"])
DailyUnique = namedtuple("DailyUnique", ["date", "unique_visitors"])


class FakeLink:
    def __init__(self, short_code, target_url):
        self.short_code = short_code
        self.target_url = target_url


class TestNormalizeLinkAnalytics:
    def test_empty_analytics(self):
        link = FakeLink("abc123", "https://example.com")
        result = normalize_link_analytics(link, 0, 0, [], [])

        assert result["short_code"] == "abc123"
        assert result["target_url"] == "https://example.com"
        assert result["totals"] == {"clicks": 0, "unique_visitors": 0}
        assert result["daily"] == []

    def test_with_totals(self):
        link = FakeLink("abc123", "https://example.com")
        result = normalize_link_analytics(link, 42, 15, [], [])

        assert result["totals"]["clicks"] == 42
        assert result["totals"]["unique_visitors"] == 15

    def test_daily_data_merged(self):
        link = FakeLink("abc123", "https://example.com")
        day1 = dt.date(2025, 3, 1)
        day2 = dt.date(2025, 3, 2)

        daily_clicks = [DailyClick(day1, 10), DailyClick(day2, 5)]
        daily_visits = [DailyUnique(day1, 3), DailyUnique(day2, 2)]

        result = normalize_link_analytics(link, 15, 5, daily_clicks, daily_visits)

        assert len(result["daily"]) == 2
        assert result["daily"][0] == {"date": "2025-03-01", "clicks": 10, "unique_visitors": 3}
        assert result["daily"][1] == {"date": "2025-03-02", "clicks": 5, "unique_visitors": 2}

    def test_dates_sorted(self):
        link = FakeLink("abc123", "https://example.com")
        day1 = dt.date(2025, 3, 5)
        day2 = dt.date(2025, 3, 1)

        # Intentionally out of order
        daily_clicks = [DailyClick(day1, 2), DailyClick(day2, 8)]
        daily_visits = []

        result = normalize_link_analytics(link, 10, 0, daily_clicks, daily_visits)

        dates = [entry["date"] for entry in result["daily"]]
        assert dates == ["2025-03-01", "2025-03-05"]

    def test_mismatched_click_and_visit_dates(self):
        """Clicks on day1, visits on day2 — both dates should appear."""
        link = FakeLink("abc123", "https://example.com")
        day1 = dt.date(2025, 3, 1)
        day2 = dt.date(2025, 3, 2)

        daily_clicks = [DailyClick(day1, 5)]
        daily_visits = [DailyUnique(day2, 2)]

        result = normalize_link_analytics(link, 5, 2, daily_clicks, daily_visits)

        assert len(result["daily"]) == 2
        assert result["daily"][0] == {"date": "2025-03-01", "clicks": 5, "unique_visitors": 0}
        assert result["daily"][1] == {"date": "2025-03-02", "clicks": 0, "unique_visitors": 2}

    def test_string_dates_are_converted(self):
        """The normalizer handles iso-format date strings for unique visits."""
        link = FakeLink("abc123", "https://example.com")
        day = dt.date(2025, 3, 1)

        daily_clicks = [DailyClick(day, 3)]
        # Some DB drivers return date as a string
        daily_visits = [DailyUnique("2025-03-01", 1)]

        result = normalize_link_analytics(link, 3, 1, daily_clicks, daily_visits)

        assert len(result["daily"]) == 1
        assert result["daily"][0]["clicks"] == 3
        assert result["daily"][0]["unique_visitors"] == 1
