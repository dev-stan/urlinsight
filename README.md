# URL Insight

A backend service that shortens URLs and passively captures link usage analytics via an API. Not just a URL shortener - it's more like a telemetry system for links.

---

## Features

- [x] Create short URLs from long URLs  
- [x] Redirect short URLs to their target URL  
- [x] Capture click events (timestamp, hashed IP, user agent, referrer)  
- [x] Track unique visitors and bot traffic per link  
- [x] Aggregate analytics per link (total clicks, clicks over time)
- [ ] Classify events (device type, browser, bot vs human)  
- [ ] Query cross-link metrics (tags, top-performing links, referrers)  
- [ ] Expose all analytics via clean API endpoints  
- [ ] Fully backend-focused; frontend is optional  


## Conceptual Overview

1. **Link creation**: Users submit a URL and receive a short code.  
2. **Redirect**: Requests to `/short_code` resolve the target URL and redirect.  
3. **Event tracking**: Every click is recorded as an event with metadata.  
4. **Analytics**: Aggregated metrics are available via API for time-series or breakdowns.  

---

## Tech Stack

- Python 3.10+  
- FastAPI  
- SQLAlchemy  
- SQLite (initially, can be swapped for Postgres)  
- Pydantic for input/output validation  

## Notes

- Redirect endpoint is synchronous and lightweight; event tracking can be optimized later.  
- All analytics are passive; no extra user input is required.  
- Designed for small-scale deployment but structured to scale with minimal changes.  


## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
