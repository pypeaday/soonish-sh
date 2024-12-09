# Soonish - Event Countdown Application

Soonish is a sleek web application that helps you track upcoming events with beautiful visual countdowns. Built with FastAPI and modern web technologies, it provides an intuitive interface for managing your important dates and events.

## Features

### Event Management
- **Create Events**: Add new events with custom names, target dates, and messages
- **Visual Countdowns**: Each event displays a live countdown showing days, hours, minutes, and seconds
- **Smart Sorting**: Events are automatically sorted by time remaining, with closest events first
- **Delete Events**: Easily remove events you no longer need
- **Event Details**: Click any event to view full details in a modal window

### Image Integration
- **Event Images**: Each event can have an associated image
- **Image Picker**: Built-in image selector with curated Unsplash images
- **Image Preview**: Preview selected images before creating an event
- **Compact Display**: Events show thumbnail-sized images (48x48px) for a clean interface

### User Interface
- **Modern Design**: Clean, modern interface with a dark theme
- **Responsive Layout**: Works well on different screen sizes
- **Interactive Elements**: Hover effects and smooth transitions
- **Modal Windows**: Detailed event view in modal overlays

### Technical Features
- **Real-time Updates**: Countdowns update in real-time
- **FastAPI Backend**: Fast and efficient Python-based backend
- **Static Image Pool**: Curated collection of Unsplash images for quick loading
- **Error Handling**: Graceful handling of image loading errors with fallbacks

## Getting Started

1. Install the required dependencies:
```bash
pip install fastapi uvicorn jinja2 python-multipart
```

2. Run the application:
```bash
uvicorn app:app --reload
```

3. Open your browser and navigate to `http://localhost:8000`

## Usage

1. **Creating an Event**:
   - Click the "Add Event" button
   - Fill in the event name and target date
   - (Optional) Add a message and select an image
   - Click "Create Event"

2. **Viewing Events**:
   - All events are displayed on the main page
   - Click any event to view full details
   - Countdowns update automatically

3. **Deleting Events**:
   - Open the event details
   - Click the "Delete" button
   - Confirm deletion when prompted

## Contributing

Feel free to submit issues and enhancement requests!
