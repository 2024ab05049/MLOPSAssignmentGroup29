"""
Startup script for Azure App Service
Azure App Service looks for app.py or startup.py
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI app
from app import app

# For Azure App Service, we can use gunicorn or uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

