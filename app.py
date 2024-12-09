from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db, DBEvent
import uvicorn
import random

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
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
    return [{"id": event.id, **event.to_dict()} for event in events]

@app.delete("/api/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        return {"status": "success", "id": event_id}
    return {"status": "not_found"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
