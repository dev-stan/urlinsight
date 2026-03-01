from app.db.models import ClickEvent, UniqueVisit


class TestRedirectSuccess:
    def test_redirects_to_target(self, client):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        resp = client.get(f"/redirect/{code}", follow_redirects=False)
        assert resp.status_code == 307
        assert resp.headers["location"] == "https://example.com"

    def test_not_found(self, client):
        resp = client.get("/redirect/bad_code", follow_redirects=False)
        assert resp.status_code == 404


class TestRedirectTracking:
    def test_creates_click_event(self, client, db):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        client.get(f"/redirect/{code}", follow_redirects=False)

        events = db.query(ClickEvent).all()
        assert len(events) == 1
        assert events[0].ip_hash is not None

    def test_creates_unique_visit(self, client, db):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        client.get(f"/redirect/{code}", follow_redirects=False)

        visits = db.query(UniqueVisit).all()
        assert len(visits) == 1

    def test_multiple_redirects_create_multiple_click_events(self, client, db):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        for _ in range(3):
            client.get(f"/redirect/{code}", follow_redirects=False)

        events = db.query(ClickEvent).all()
        assert len(events) == 3

    def test_same_ip_only_one_unique_visit_per_day(self, client, db):
        """TestClient uses the same IP (testclient), so multiple
        redirects should create only one unique visit per day."""
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        for _ in range(3):
            client.get(f"/redirect/{code}", follow_redirects=False)

        visits = db.query(UniqueVisit).all()
        assert len(visits) == 1

    def test_captures_user_agent(self, client, db):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        client.get(
            f"/redirect/{code}",
            headers={"user-agent": "CustomBot/1.0"},
            follow_redirects=False,
        )

        event = db.query(ClickEvent).first()
        assert event.user_agent == "CustomBot/1.0"

    def test_captures_referrer(self, client, db):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        client.get(
            f"/redirect/{code}",
            headers={"referer": "https://twitter.com/post/123"},
            follow_redirects=False,
        )

        event = db.query(ClickEvent).first()
        assert event.referrer == "https://twitter.com/post/123"
