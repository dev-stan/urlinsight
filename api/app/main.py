from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from sqlalchemy import inspect, text

from app.api.routers import auth, links, redirect
from app.db.database import Base, engine
from app.middleware import rate_limiter

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "web" / "build"


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

# Mount all API routes under /api prefix
api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(links.router)
api_router.include_router(redirect.router)
app.include_router(api_router)


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve SvelteKit static build with SPA fallback."""
    if not STATIC_DIR.is_dir():
        return Response(content="Frontend not built", status_code=404)

    # Try to serve the exact file
    file_path = STATIC_DIR / full_path
    if file_path.is_file():
        return FileResponse(str(file_path))

    # Try index.html inside a directory
    index_path = file_path / "index.html"
    if file_path.is_dir() and index_path.is_file():
        return FileResponse(str(index_path))

    # SPA fallback
    fallback = STATIC_DIR / "200.html"
    if fallback.is_file():
        return FileResponse(str(fallback))

    return Response(content="Not found", status_code=404)
