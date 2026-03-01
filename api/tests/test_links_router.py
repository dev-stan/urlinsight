from app.db.models import Link


class TestCreateLink:
    def test_success_anonymous(self, client):
        resp = client.post("/links", json={"target_url": "https://example.com"})
        assert resp.status_code == 200
        data = resp.json()
        assert "short_code" in data
        assert data["target_url"] == "https://example.com"
        assert len(data["short_code"]) == 6

    def test_anonymous_link_has_no_user(self, client, db):
        resp = client.post("/links", json={"target_url": "https://example.com"})
        code = resp.json()["short_code"]
        link = db.query(Link).filter(Link.short_code == code).first()
        assert link.user_id is None

    def test_authenticated_link_has_user_id(self, auth_client, db, sample_user):
        resp = auth_client.post("/links", json={"target_url": "https://example.com"})
        code = resp.json()["short_code"]
        link = db.query(Link).filter(Link.short_code == code).first()
        assert link.user_id == sample_user.id

    def test_returns_different_codes(self, client):
        codes = set()
        for _ in range(5):
            resp = client.post("/links", json={"target_url": "https://example.com"})
            codes.add(resp.json()["short_code"])
        assert len(codes) == 5


class TestListLinks:
    def test_requires_auth(self, client):
        resp = client.get("/links")
        assert resp.status_code == 401

    def test_empty_list(self, auth_client):
        resp = auth_client.get("/links")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_only_own_links(self, auth_client, db, sample_user):
        # Create a link as authenticated user
        auth_client.post("/links", json={"target_url": "https://mine.com"})

        # Create an anonymous link (should not appear)
        other_link = Link(short_code="other1", target_url="https://other.com")
        db.add(other_link)
        db.commit()

        resp = auth_client.get("/links")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["target_url"] == "https://mine.com"


class TestGetLink:
    def test_existing_link(self, client):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        resp = client.get(f"/links/{code}")
        assert resp.status_code == 200
        assert resp.json()["short_code"] == code
        assert resp.json()["target_url"] == "https://example.com"

    def test_not_found(self, client):
        resp = client.get("/links/nonexistent")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Link not found"


class TestLinkAnalytics:
    def test_analytics_no_events(self, client):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        resp = client.get(f"/links/{code}/analytics")
        assert resp.status_code == 200
        data = resp.json()
        assert data["short_code"] == code
        assert data["totals"]["clicks"] == 0
        assert data["totals"]["unique_visitors"] == 0
        assert data["daily"] == []

    def test_analytics_after_redirect(self, client):
        create_resp = client.post("/links", json={"target_url": "https://example.com"})
        code = create_resp.json()["short_code"]

        # Trigger a redirect (generates click + unique visit)
        client.get(f"/redirect/{code}", follow_redirects=False)

        resp = client.get(f"/links/{code}/analytics")
        data = resp.json()
        assert data["totals"]["clicks"] == 1
        assert data["totals"]["unique_visitors"] == 1
        assert len(data["daily"]) == 1

    def test_analytics_not_found(self, client):
        resp = client.get("/links/nope/analytics")
        assert resp.status_code == 404
