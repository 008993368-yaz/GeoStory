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
- `DATABASE_URL`: PostgreSQL connection string (format: `postgresql://user:password@host:port/database`)

## Database Migrations

GeoStory uses Alembic for database schema management.

### Prerequisites

Ensure you have PostgreSQL installed and running, and that you've set the `DATABASE_URL` in your `.env` file:

```bash
DATABASE_URL=postgresql://ls_user:password@localhost:5432/geostory
```

### Running Migrations

Apply all pending migrations to bring your database up to date:

**Windows (PowerShell):**
```powershell
.\scripts\run_migrations.ps1
```

**Linux/macOS (Bash):**
```bash
# Make the migration script executable (first time only)
chmod +x scripts/run_migrations.sh

# Run migrations
./scripts/run_migrations.sh
```

**Alternative (all platforms):**
```bash
alembic -c alembic.ini upgrade head
```

The migration script will:
1. Load environment variables from `.env`
2. Verify `DATABASE_URL` is set
3. Show the current database revision
4. Apply all pending migrations
5. Display the new current revision

### Useful Migration Commands

```bash
# Check current database revision
alembic -c alembic.ini current

# View migration history
alembic -c alembic.ini history

# Rollback the last migration
alembic -c alembic.ini downgrade -1

# Rollback all migrations
alembic -c alembic.ini downgrade base

# Generate a new migration (after modifying models)
alembic -c alembic.ini revision --autogenerate -m "description of changes"

# Manually create a new migration file
alembic -c alembic.ini revision -m "description of changes"
```

### Initial Migration

The initial migration (`20260125_120000_initial_tables.py`) creates:
- **users** table: For optional user authentication (email nullable for anonymous stories)
- **stories** table: Core location-based stories with lat/lng validation and constraints
- **photos** table: Photo metadata with foreign key to stories (images stored in GCS)
- **Indexes**: Optimized for timeline queries, category filtering, and photo ordering
- **Trigger**: Auto-updates `stories.updated_at` on modifications
- **Extension**: pgcrypto for UUID generation

See `docs/schema.md` and `docs/schema.sql` for detailed schema documentation.

### Migration Notes

- Migrations use synchronous SQLAlchemy connections (standard for DDL operations)
- The `DATABASE_URL` must use the `postgresql://` scheme (not `postgresql+asyncpg://`)
- Alembic tracks applied migrations in the `alembic_version` table
- Always test migrations on a development database before applying to production

### Docker Compose Database Setup

If using Docker Compose for local development, you can run migrations after starting the database:

```bash
# Start the database service
docker-compose -f docker-compose.dev.yml up -d db

# Wait for database to be ready, then run migrations
./scripts/run_migrations.sh

# Or run migrations inside the backend container
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
```

## Next Steps

- ✅ Database schema and migrations
- ✅ SQLAlchemy ORM models
- ✅ Story CRUD endpoints
- ✅ Backend testing infrastructure
- Implement authentication
- Add photo upload endpoints

## Running Tests

GeoStory uses pytest with an isolated test database for reliable testing.

### Prerequisites

- Docker and Docker Compose installed
- Backend dependencies installed (`pip install -r requirements.txt`)

### Quick Start

Run the full test suite with the provided test runner:

**Windows (PowerShell):**
```powershell
.\scripts\run_tests.ps1
```

**Linux/macOS (Bash):**
```bash
# Make the test script executable (first time only)
chmod +x scripts/run_tests.sh

# Run tests
./scripts/run_tests.sh
```

The test runner will:
1. Start an isolated PostgreSQL test database on port 5433
2. Wait for the database to be ready
3. Run database migrations
4. Execute all tests with verbose output
5. Report results

### Manual Testing

If you want more control over the testing process:

```bash
# 1. Start the test database
docker-compose -f docker-compose.test.yml up -d

# 2. Wait for database to be ready
docker-compose -f docker-compose.test.yml exec -T db_test pg_isready -U geostory_user -d geostory_test

# 3. Set environment variable and run migrations
export TEST_DATABASE_URL="postgresql+asyncpg://geostory_user:geostory_pass@localhost:5433/geostory_test"
export DATABASE_URL="$TEST_DATABASE_URL"
alembic upgrade head

# 4. Run tests
pytest tests/ -v

# 5. Cleanup (optional)
docker-compose -f docker-compose.test.yml down
```

### Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_create_story.py -v

# Run a specific test function
pytest tests/test_create_story.py::test_create_story_success -v

# Run tests matching a pattern
pytest tests/ -k "create" -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html
```

### Test Database

The test database:
- Runs in Docker on port 5433 (separate from dev database on 5432)
- Uses database name: `geostory_test`
- Credentials: `geostory_user` / `geostory_pass`
- Automatically truncates tables between tests for isolation
- Managed by fixtures in `tests/conftest.py`

### Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures (db, client)
├── test_health.py           # Health check endpoint tests
├── test_create_story.py     # POST /api/stories tests
├── test_get_story.py        # GET /api/stories/{id} tests
├── test_list_stories.py     # GET /api/stories tests
├── test_story_schema.py     # Pydantic schema validation tests
└── test_validation.py       # Input validation tests
```

### Environment Variables for Testing

- `TEST_DATABASE_URL`: PostgreSQL connection string for tests (default: `postgresql+asyncpg://geostory_user:geostory_pass@localhost:5433/geostory_test`)

### Troubleshooting Tests

**Database connection errors:**
```bash
# Check if test database is running
docker ps | grep geostory_test

# View test database logs
docker-compose -f docker-compose.test.yml logs db_test

# Restart test database
docker-compose -f docker-compose.test.yml restart
```

**Migration errors:**
```bash
# Reset test database completely
docker-compose -f docker-compose.test.yml down -v
docker-compose -f docker-compose.test.yml up -d
alembic upgrade head
```

**Port conflicts:**
```bash
# Check what's using port 5433
netstat -ano | findstr :5433  # Windows
lsof -i :5433                 # macOS/Linux

# Stop conflicting service or change port in docker-compose.test.yml
```
