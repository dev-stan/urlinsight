from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.auth import create_access_token
from app.db.database import Base, get_db
from app.db.models import ClickEvent, Link, UniqueVisit
from app.main import app
from app.services.users.queries import create_user

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def _setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def _mock_redis(monkeypatch):
    """Bypass Redis-backed rate limiter in tests."""
    mock_client = AsyncMock()
    mock_client.incr.return_value = 1
    mock_client.pexpire.return_value = True
    monkeypatch.setattr("app.middleware.rate_limiter.redis_client", mock_client)


@pytest.fixture()
def db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def sample_user(db):
    return create_user(db, "test@example.com", "testpassword123")


@pytest.fixture()
def auth_client(client, sample_user):
    """A test client with a valid JWT Authorization header."""
    token = create_access_token(sample_user.id)
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture()
def sample_link(db):
    link = Link(short_code="abc123", target_url="https://example.com")
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@pytest.fixture()
def sample_link_with_events(db, sample_link):
    """A link that already has click events and unique visits."""
    from datetime import date

    for i in range(3):
        db.add(
            ClickEvent(
                link_id=sample_link.id,
                ip_hash=f"hash_{i}",
                user_agent="Mozilla/5.0",
                referrer="https://google.com",
            )
        )

    db.add(UniqueVisit(link_id=sample_link.id, ip_hash="hash_0", date=date.today()))
    db.add(
        UniqueVisit(
            link_id=sample_link.id,
            ip_hash="hash_1",
            date=date.today(),
        )
    )
    db.commit()
    return sample_link
