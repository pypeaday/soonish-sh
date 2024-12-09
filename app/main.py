from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Event(BaseModel):
    name: str
    target_time: datetime
    image_url: str
    message: str

# Sample events
countdown_events = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "events": countdown_events})

@app.post("/create_event")
async def create_event(name: str = Form(...), target_time: str = Form(...), image_url: str = Form(...), message: str = Form(...)):
    event = Event(name=name, target_time=datetime.fromisoformat(target_time), image_url=image_url, message=message)
    countdown_events.append(event)
    return templates.TemplateResponse("index.html", {"request": Request, "events": countdown_events})

@app.get("/event/{event_id}", response_class=HTMLResponse)
async def get_event(request: Request, event_id: int):
    event = countdown_events[event_id]
    return templates.TemplateResponse("event.html", {"request": request, "event": event})
