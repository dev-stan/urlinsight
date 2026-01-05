from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Link
from schemas import LinkCreate, LinkResponse
import string, random
from dependencies import get_link_or_404
from contextlib import asynccontextmanager
from database import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield  # needed for contextmanager

app = FastAPI(lifespan=lifespan)

# Helper: generate random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/links", response_model=LinkResponse)
def create_link(link_in: LinkCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    # Ensure uniqueness (simple retry loop)
    while db.query(Link).filter(Link.short_code == short_code).first():
        short_code = generate_short_code()

    link = Link(short_code=short_code, target_url=link_in.target_url)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

@app.get("/links", response_model=list[LinkResponse])
def list_links(db: Session = Depends(get_db)):
    links = db.query(Link).all()
    return links

@app.get("/links/{short_code}", response_model=LinkResponse)
def get_link(short_code: str, db: Session = Depends(get_db), link: Link = Depends(get_link_or_404)):
    return link

@app.get("/redirect/{short_code}", response_class=RedirectResponse, status_code=302)
def redirect_link(short_code: str, db: Session = Depends(get_db), link: Link = Depends(get_link_or_404)):
    return link.target_url

