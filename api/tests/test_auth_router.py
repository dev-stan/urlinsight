class TestRegister:
    def test_success(self, client):
        resp = client.post(
            "/auth/register",
            json={"email": "new@example.com", "password": "strongpass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "new@example.com"
        assert "id" in data
        assert "password" not in data

    def test_duplicate_email(self, client):
        payload = {"email": "dup@example.com", "password": "pass123"}
        client.post("/auth/register", json=payload)
        resp = client.post("/auth/register", json=payload)
        assert resp.status_code == 409
        assert resp.json()["detail"] == "Email already registered"


class TestLogin:
    def test_success(self, client):
        client.post(
            "/auth/register",
            json={"email": "login@example.com", "password": "mypassword"},
        )
        resp = client.post(
            "/auth/login",
            json={"email": "login@example.com", "password": "mypassword"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_wrong_password(self, client):
        client.post(
            "/auth/register",
            json={"email": "user@example.com", "password": "correct"},
        )
        resp = client.post(
            "/auth/login",
            json={"email": "user@example.com", "password": "wrong"},
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Invalid email or password"

    def test_nonexistent_user(self, client):
        resp = client.post(
            "/auth/login",
            json={"email": "ghost@example.com", "password": "whatever"},
        )
        assert resp.status_code == 401


class TestGetMe:
    def test_authenticated(self, auth_client):
        resp = auth_client.get("/auth/me")
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_no_token(self, client):
        resp = client.get("/auth/me")
        assert resp.status_code == 401

    def test_invalid_token(self, client):
        client.headers["Authorization"] = "Bearer invalid.jwt.token"
        resp = client.get("/auth/me")
        assert resp.status_code == 401
