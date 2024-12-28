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

# Update main.py
from unsplash.photo import Photo
from unsplash.models import Photo as PhotoModel

# Initialize API first
auth = Auth(
    os.getenv('UNSPLASH_ACCESS_KEY'),
    os.getenv('UNSPLASH_SECRET_KEY'),
    redirect_uri=""
)

api = Api(auth)

# Define the new search method
def custom_search(self, query, category=None, orientation=None, page=1, per_page=10):
    logger.info(f"Custom search with query: {query}")
    if orientation and orientation not in self.orientation_values:
        raise Exception()
    
    params = {
        "query": query,
        "category": category,
        "orientation": orientation,
        "page": page,
        "per_page": per_page
    }
    url = "/search/photos"
    logger.info(f"Making request to {url} with params: {params}")
    _result = self._get(url, params=params)
    logger.info(f"Raw API response: {_result}")
    result = _result.get("results", [])
    logger.info(f"Extracted results: {result}")
    return PhotoModel.parse_list(result)

# Monkey patch the search method directly onto the existing photo instance
import types
api.photo.search = types.MethodType(custom_search, api.photo)

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
    
    events = db.query(DBEvent).all()
    return templates.TemplateResponse(
        "partials/events_partial.html",
        {"request": request, "events": events, "now": datetime.now()}
    )

@app.get("/create-form")
async def get_create_form(request: Request):
    return templates.TemplateResponse(
        "partials/create_form.html",
        {"request": request}
    )

@app.get("/random_images")
async def get_random_images():
    photos = api.photo.random(count=1)
    if photos:
        photo = photos[0]
        return HTMLResponse(photo.urls.regular)
    return HTMLResponse(random.choice(DEFAULT_IMAGES))

@app.get("/api/events")
async def get_events(request: Request, db: Session = Depends(get_db)):
    events = db.query(DBEvent).all()
    return templates.TemplateResponse(
        "partials/events_partial.html",
        {"request": request, "events": events, "now": datetime.now()}
    )

@app.get("/event/{event_id}")
async def get_event(event_id: int, request: Request, db: Session = Depends(get_db)):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return templates.TemplateResponse(
        "event_edit.html",
        {"request": request, "event": event}
    )

@app.put("/event/{event_id}")
async def update_event(
    event_id: int,
    request: Request,
    name: str = Form(...),
    target_time: str = Form(...),
    image_url: str = Form(""),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.name = name
    event.target_time = datetime.fromisoformat(target_time)
    event.image_url = image_url
    event.message = message
    
    db.commit()
    
    events = db.query(DBEvent).all()
    return templates.TemplateResponse(
        "partials/events_partial.html",
        {"request": request, "events": events, "now": datetime.now()}
    )

@app.delete("/event/{event_id}")
async def delete_event(event_id: int, request: Request, db: Session = Depends(get_db)):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    
    events = db.query(DBEvent).all()
    return templates.TemplateResponse(
        "partials/events_partial.html",
        {"request": request, "events": events, "now": datetime.now()}
    )
import requests

@app.get("/search_images")
async def search_images(query: str):
    try:
        # Direct API call to Unsplash
        access_key = os.getenv('UNSPLASH_ACCESS_KEY')
        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {access_key}"
        }
        params = {
            "query": query,
            "per_page": 3
        }
        
        logger.info(f"Making direct request to Unsplash API: {url}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Raw API response: {data}")
        
        photos = []
        for photo in data.get('results', []):
            try:
                photo_dict = {
                    "url": photo['urls']['regular'],
                    "thumb": photo['urls']['thumb']
                }
                photos.append(photo_dict)
                logger.info(f"Added photo: {photo_dict}")
            except Exception as e:
                logger.error(f"Error processing photo: {e}")
                continue
        
        return JSONResponse(content={"photos": photos})
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )