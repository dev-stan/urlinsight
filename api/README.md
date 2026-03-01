# URL Insight

A backend service that shortens URLs and passively captures link usage analytics via an API. Not a URL shortener — it's a telemetry system for links.

---

## Features

- Short URL creation with unique code generation
- Redirect with passive click event tracking (timestamp, hashed IP, user agent, referrer)
- Unique visitor tracking per link per day
- Aggregated analytics (total clicks, unique visitors, daily time-series)
- Window-based rate limiting via Redis
- Clean REST API with auto-generated OpenAPI docs

## How It Works

1. **Link creation** — Submit a URL, receive a short code.
2. **Redirect** — Requests to `/redirect/{short_code}` resolve and redirect to the target URL.
3. **Event capture** — Every redirect records a click event with request metadata.
4. **Analytics** — Aggregated metrics are exposed via API for totals and daily breakdowns.

---

## Tech Stack

- **Python 3.10+** with **FastAPI**
- **SQLAlchemy** ORM with SQLite (swappable for PostgreSQL)
- **Pydantic** for request/response validation and settings management
- **Redis** for rate limiting
- **Ruff** for linting and formatting
- **GitHub Actions** CI pipeline

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/links` | Create a short link |
| `GET` | `/links` | List all links |
| `GET` | `/links/{short_code}` | Get a specific link |
| `GET` | `/links/{short_code}/analytics` | Get click and visitor analytics |
| `GET` | `/redirect/{short_code}` | Redirect to target URL |

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the project
pip install .

# Install with dev dependencies (ruff, pytest)
pip install ".[dev]"

# Copy the example env and configure
cp .env.example .env

# Run the app
uvicorn app.main:app --reload
```

## Development

```bash
# Lint
ruff check .

# Format
ruff format .

# Run tests ( i'm yet to add those! not looking forward to this )
pytest
```

## Project Structure

```
app/
  main.py              # FastAPI application entry point
  api/
    deps.py            # Shared dependencies (e.g. get_link_or_404)
    routers/
      links.py         # Link CRUD and analytics endpoints
      redirect.py      # Short URL redirect with event capture
  core/
    config.py          # Pydantic settings (env-based configuration)
    security.py        # IP hashing (HMAC-SHA256)
  db/
    database.py        # SQLAlchemy engine and session setup
    models.py          # ORM models (Link, ClickEvent, UniqueVisit)
  middleware/
    rate_limiter.py    # Redis-backed sliding window rate limiter
  schemas/
    link.py            # Pydantic request/response schemas
  services/
    click_events/      # Click event creation logic
    links/             # Link queries, analytics normalization, utils
    unique_visits/     # Unique visitor tracking with deduplication
```
