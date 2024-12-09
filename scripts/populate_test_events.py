#!/usr/bin/env python3

import httpx
from datetime import datetime, timedelta
import pytz

# Convert Central Time (current time zone) to UTC for consistency
central = pytz.timezone('America/Chicago')
base_time = central.localize(datetime(2024, 12, 9, 6, 8, 45))  # Using provided current time

# Test events with their relative dates and Unsplash image keywords
events = [
    {
        "name": "Winter Cabin Retreat",
        "days_from_now": 15,
        "message": "A cozy weekend in a snow-covered cabin with hot chocolate and board games",
        "image_keyword": "winter-cabin"
    },
    {
        "name": "Summer Music Festival",
        "days_from_now": 180,
        "message": "Three days of amazing live music under the stars",
        "image_keyword": "music-festival"
    },
    {
        "name": "Spa Day Relaxation",
        "days_from_now": 7,
        "message": "A full day of massages, facials, and pure relaxation",
        "image_keyword": "spa-relaxation"
    },
    {
        "name": "Beach Sunrise Yoga",
        "days_from_now": 30,
        "message": "Morning yoga session followed by breakfast on the beach",
        "image_keyword": "beach-sunrise"
    },
    {
        "name": "Mountain Hiking Adventure",
        "days_from_now": 45,
        "message": "Epic day hike with stunning views and picnic at the summit",
        "image_keyword": "mountain-hiking"
    }
]

def get_unsplash_image(keyword: str) -> str:
    # Using Unsplash Source API for demo images
    return f"https://source.unsplash.com/featured/?{keyword}"

def create_event(event_data: dict) -> None:
    target_time = base_time + timedelta(days=event_data["days_from_now"])
    
    # Create form data instead of JSON
    form_data = {
        "name": event_data["name"],
        "target_time": target_time.isoformat(),  # Use ISO format as expected by the API
        "message": event_data["message"],
        "image_url": get_unsplash_image(event_data["image_keyword"])
    }
    
    try:
        # Using form data with the correct endpoint and port 8002
        response = httpx.post("http://localhost:8002/create_event", data=form_data)
        if response.status_code == 200:
            print(f"Successfully created event: {form_data['name']}")
        else:
            print(f"Failed to create event: {form_data['name']} - Status: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Request data: {form_data}")  # Add this for debugging
    except Exception as e:
        print(f"Error creating event {form_data['name']}: {str(e)}")

def main():
    print("Creating test events...")
    for event_data in events:
        create_event(event_data)
    print("Done!")

if __name__ == "__main__":
    main()
