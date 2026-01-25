# GeoStory Backend

Minimal FastAPI backend for the GeoStory project.

## Requirements

- Python 3.11 or higher
- pip

## Setup

### 1. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and edit as needed:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

## Running the Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing the Health Endpoint

Test that the API is running correctly:

### Using a browser:
Navigate to: `http://localhost:8000/api/health`

### Using curl:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "ok"
}
```

## API Documentation

Once the server is running, view the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app with health endpoint
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
└── README.md           # This file
```

## Environment Variables

- `APP_ENV`: Application environment (default: `development`)
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins (default: `http://localhost:5173`)

## Next Steps

- Add database models and migrations
- Implement authentication
- Add story CRUD endpoints
- Set up file uploads for media
