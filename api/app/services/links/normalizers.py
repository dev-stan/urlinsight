# services/analytics/normalizers.py
import datetime as dt


def normalize_link_analytics(link, total_clicks, total_unique_visits, daily_clicks, daily_unique_visits):
    clicks_by_date = {row.date: row.clicks for row in daily_clicks}
    uniques_by_date = {
        row.date if isinstance(row.date, dt.date) else dt.date.fromisoformat(row.date): row.unique_visitors
        for row in daily_unique_visits
    }

    all_dates = sorted(set(clicks_by_date.keys()) | set(uniques_by_date.keys()))

    daily = [
        {"date": d.isoformat(), "clicks": clicks_by_date.get(d, 0), "unique_visitors": uniques_by_date.get(d, 0)}
        for d in all_dates
    ]

    return {
        "short_code": link.short_code,
        "target_url": link.target_url,
        "totals": {"clicks": total_clicks, "unique_visitors": total_unique_visits},
        "daily": daily,
    }
