from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    name: str
    target_time: datetime
    image_url: str
    message: str
