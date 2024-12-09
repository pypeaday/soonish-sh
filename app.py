import uvicorn
import os

# Get port from environment variable, default to 8000
port = int(os.getenv('SOONISH_PORT', '8000'))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
