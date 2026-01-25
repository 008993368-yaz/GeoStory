# Development Dockerfile for GeoStory Backend
# For production, use multi-stage builds, non-root user, and optimize layers

FROM python:3.11-slim

# Prevents Python from buffering stdout/stderr
# Ensures logs appear in real-time in Docker
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start uvicorn with auto-reload for development
# --reload watches for file changes and restarts server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
