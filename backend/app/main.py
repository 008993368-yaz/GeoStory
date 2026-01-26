from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="GeoStory API",
    version="0.1.0",
    debug=settings.DEBUG,
)

# Configure CORS middleware
# Allows the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
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
