import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="GeoStory API", version="0.1.0")

# Configure CORS middleware
# Allows the frontend to communicate with the backend
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
# Used to verify the API is running correctly
@app.get("/api/health")
async def health_check():
    """Return the health status of the API."""
    return {"status": "ok"}
