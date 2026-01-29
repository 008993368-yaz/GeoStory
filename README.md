# GeoStory

A location-based storytelling platform where users can pin personal stories to real-world places. Built as a full-stack portfolio project demonstrating modern web development with geospatial capabilities.

---

## 🎯 Project Summary

GeoStory enables users to create and explore stories anchored to geographic locations. Users can browse stories on an interactive map, filter by category or date, and contribute their own location-tagged narratives.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + TypeScript, Vite, React Router |
| **UI Components** | Esri Calcite Design System |
| **Mapping** | ArcGIS JS API (@arcgis/core) |
| **Backend** | FastAPI (Python 3.11), async SQLAlchemy |
| **Database** | PostgreSQL 15 with Alembic migrations |
| **DevOps** | Docker Compose, Nginx (planned) |
| **Storage** | Google Cloud Storage (planned for photos) |
| **Testing** | pytest (backend), Vitest (frontend) |

## ✅ Features Implemented

### Frontend
- **Interactive Map** - ArcGIS-powered map with story pins and bidirectional selection
- **Story List** - Grid and timeline view modes with visual feedback
- **Filters & Search** - Category filter, date range filter, keyword search
- **Pagination** - Load more stories with URL-based state preservation
- **Create Story Form** - Map-based location picker, category selection, validation
- **Responsive Design** - Calcite Design System with CSS design tokens

### Backend
- **REST API** - FastAPI with full OpenAPI documentation
- **CRUD Operations** - Create, read, list stories with filtering/pagination
- **Async Database** - SQLAlchemy 2.0 with asyncpg driver
- **Data Validation** - Pydantic schemas with custom validators
- **Database Migrations** - Alembic with proper versioning

### Testing
- **Backend** - 100 pytest tests with full DB isolation
- **Frontend** - Vitest smoke tests for Home and StoryCreate pages

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ (for frontend)
- **Python** 3.11+ (for backend)
- **PostgreSQL** 15+ (or use Docker)
- **Docker & Docker Compose** (optional, for containerized setup)

### Option 1: Run with Docker Compose (Recommended)

```bash
# Clone and enter project
cd GeoStory

# Copy environment file
cp .env.dev.example .env.dev

# Start all services (frontend, backend, database)
docker compose -f docker-compose.dev.yml up --build

# Access the app
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/docs
```

### Option 2: Run Locally

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# App available at http://localhost:3000
```

---

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Using the test script (recommended)
# Windows:
.\scripts\run_tests.ps1

# Linux/macOS:
./scripts/run_tests.sh

# Or with pytest directly (requires test database)
docker compose -f docker-compose.test.yml up -d
pytest -v
```

**Test Coverage:**
- 100 tests covering CRUD operations, validation, and edge cases
- Full database isolation with per-test transactions
- Async SQLAlchemy patterns tested

### Frontend Tests

```bash
cd frontend

# Run tests in watch mode
npm run test

# Run tests once (CI mode)
npm run test:ci
```

**Test Coverage:**
- 9 smoke tests for Home and StoryCreate pages
- Mocked ArcGIS and Calcite components
- API service mocking with Vitest

---

## 📡 API Reference

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/stories` | Create a new story |
| `GET` | `/stories` | List stories (with filters) |
| `GET` | `/stories/{id}` | Get story by ID |

### Create Story

```bash
curl -X POST http://localhost:8000/api/stories \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Story",
    "body": "This happened here...",
    "category": "personal",
    "location_lat": 34.0522,
    "location_lng": -118.2437
  }'
```

### List Stories

```bash
# Basic listing
curl http://localhost:8000/api/stories

# With filters
curl "http://localhost:8000/api/stories?category=personal&limit=10&offset=0"

# With search
curl "http://localhost:8000/api/stories?search=adventure"
```

### API Documentation

Interactive docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📸 Screenshots

### Home Page - Map & Story List
![Home Page](docs/screenshots/home-map-list.png)
*Interactive map with story pins and grid/timeline list view*

### Create Story Form
![Create Story](docs/screenshots/story-create.png)
*Map-based location picker with category selection*

> 📝 *Note: Add screenshots to `docs/screenshots/` folder*

---

## 📁 Project Structure

```
GeoStory/
├── frontend/                 # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/           # Home, StoryCreate
│   │   ├── components/      # StoryCard, MapView, etc.
│   │   ├── services/        # API client, stories service
│   │   └── types/           # TypeScript interfaces
│   └── package.json
│
├── backend/                  # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── routers/         # API endpoints
│   │   ├── crud/            # Database operations
│   │   ├── schemas/         # Pydantic models
│   │   └── db/              # ORM models, session
│   ├── alembic/             # Database migrations
│   └── tests/               # pytest test suite
│
├── docs/                     # Documentation
│   ├── schema.md            # Database schema docs
│   └── ARCHITECTURE.md      # Technical design
│
└── docker-compose.dev.yml   # Development stack
```

---

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - Technical design and data flow
- [Interview Notes](INTERVIEW_NOTES.md) - Talking points and demo script
- [Backend README](backend/README.md) - API details and migrations
- [Frontend README](frontend/README.md) - Component structure and testing
- [Database Schema](docs/schema.md) - Table definitions and constraints

---

## 🗺️ Roadmap

- [ ] **Photo Uploads** - GCS integration with presigned URLs
- [ ] **Authentication** - OAuth2 with JWT tokens
- [ ] **Map Clustering** - Performance optimization for many pins
- [ ] **Production Deployment** - Nginx reverse proxy, HTTPS
- [ ] **Edit/Delete Stories** - Full CRUD for story authors

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.
