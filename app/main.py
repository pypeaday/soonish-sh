from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from .database import get_db, DBEvent
import uvicorn
import random
import logging
import os

from unsplash.api import Api
from unsplash.auth import Auth
from dotenv import load_dotenv

load_dotenv()

# Initialize logger
logger = logging.getLogger(__name__)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Add debug logging
logger.info(f"Unsplash Access Key: {os.getenv('UNSPLASH_ACCESS_KEY')[:8]}...")

auth = Auth(
    os.getenv('UNSPLASH_ACCESS_KEY'),
    os.getenv('UNSPLASH_SECRET_KEY'),
    redirect_uri=""
)


api = Api(auth)

# Initialize logger
logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates - adjust path relative to app directory
templates = Jinja2Templates(directory="app/templates")

# List of beautiful countdown-themed Unsplash images
DEFAULT_IMAGES = [
    "https://images.unsplash.com/photo-1501139083538-0139583c060f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1557180295-76eee20ae8aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1508962914676-134849a727f0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1465929639680-64ee080eb3ed?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1518281420975-50db6e5d0a97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
]

class Event(BaseModel):
    name: str
    target_time: datetime
    image_url: str = ""
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    events = db.query(DBEvent).all()
    logger.info(f"Found {len(events)} events in database")
    return templates.TemplateResponse("index.html", {"request": request, "events": events})

@app.post("/create_event")
async def create_event(
    request: Request,
    name: str = Form(...),
    target_time: str = Form(...),
    image_url: str = Form(""),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    # If no image URL provided, pick a random one from our collection
    if not image_url or image_url.strip() == "":
        image_url = random.choice(DEFAULT_IMAGES)

    db_event = DBEvent(
        name=name,
        target_time=datetime.fromisoformat(target_time),
        image_url=image_url,
        message=message
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return {"status": "success", "id": db_event.id}

@app.get("/api/events")
async def get_events(db: Session = Depends(get_db)):
    events = db.query(DBEvent).all()
    logger.info(f"Found {len(events)} events in database")
    return [{"id": event.id, **event.to_dict()} for event in events]

@app.get("/api/events/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    logger.info(f"Found event {event_id} in database")
    return event.to_dict()

@app.put("/api/events/{event_id}")
async def update_event(
    event_id: int,
    name: str = Form(...),
    target_time: str = Form(...),
    image_url: str = Form(""),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # If no image URL provided, keep the existing one or pick a random one
    if not image_url or image_url.strip() == "":
        if not event.image_url:
            image_url = random.choice(DEFAULT_IMAGES)
        else:
            image_url = event.image_url

    # Update event fields
    event.name = name
    event.target_time = datetime.fromisoformat(target_time)
    event.image_url = image_url
    event.message = message

    db.commit()
    db.refresh(event)
    logger.info(f"Updated event {event_id} in database")
    return {"status": "success", "id": event.id}

@app.delete("/api/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        logger.info(f"Deleted event {event_id} from database")
        return {"status": "success", "id": event_id}
    return {"status": "not_found"}

@app.get("/random_images")
async def get_random_images():
    photos = api.photo.random(count=2)
    return [{
        "urls": {
            "small": photo.urls.small,
            "regular": photo.urls.regular
        },
        "alt_description": photo.alt_description or "Random image"
    } for photo in photos]

