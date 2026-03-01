from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.api.routers import auth, links, redirect
from app.db.database import Base, engine
from app.middleware import rate_limiter


def _run_migrations(bind):
    """Add columns that may be missing from an older schema."""
    inspector = inspect(bind)

    if "users" not in inspector.get_table_names():
        Base.metadata.tables["users"].create(bind=bind)

    link_cols = {c["name"] for c in inspector.get_columns("links")}
    if "user_id" not in link_cols:
        with bind.begin() as conn:
            conn.execute(text("ALTER TABLE links ADD COLUMN user_id INTEGER REFERENCES users(id)"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _run_migrations(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limiter.rate_limiter_handler)

app.include_router(auth.router)
app.include_router(links.router)
app.include_router(redirect.router)
