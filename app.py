import uvicorn
import os

# Get port from environment variable, default to 8002
port = int(os.getenv('SOONISH_PORT', '8002'))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
