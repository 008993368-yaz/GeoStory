# Alembic Migration Setup - Quick Reference

## What Was Created

### Core Alembic Files
- ✅ `backend/alembic.ini` - Alembic configuration
- ✅ `backend/alembic/env.py` - Environment setup (loads DATABASE_URL from .env)
- ✅ `backend/alembic/script.py.mako` - Migration file template
- ✅ `backend/alembic/versions/20260125_120000_initial_tables.py` - Initial schema migration

### Helper Scripts
- ✅ `backend/scripts/run_migrations.ps1` - PowerShell migration runner (Windows)
- ✅ `backend/scripts/run_migrations.sh` - Bash migration runner (Linux/macOS)

### Updated Files
- ✅ `backend/requirements.txt` - Added alembic, psycopg2-binary, sqlalchemy
- ✅ `backend/.env.example` - Added DATABASE_URL example
- ✅ `backend/README.md` - Added comprehensive migration documentation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file (copy from `.env.example`):
```env
DATABASE_URL=postgresql://ls_user:password@localhost:5432/geostory
```

### 3. Run Migrations
**Windows:**
```powershell
.\scripts\run_migrations.ps1
```

**Linux/macOS:**
```bash
chmod +x scripts/run_migrations.sh
./scripts/run_migrations.sh
```

## What the Migration Creates

The initial migration (`20260125_120000_initial_tables.py`) sets up:

### Extensions
- `pgcrypto` - For `gen_random_uuid()` function

### Tables
1. **users**
   - `id` (UUID, primary key)
   - `email` (TEXT, unique, nullable)
   - `created_at` (TIMESTAMPTZ)

2. **stories**
   - `id` (UUID, primary key)
   - `owner_id` (UUID, FK → users.id, nullable, ON DELETE SET NULL)
   - `title` (TEXT, not null)
   - `body` (TEXT, nullable)
   - `category` (TEXT, CHECK constraint for valid values)
   - `location_lat` (DOUBLE PRECISION, -90 to 90)
   - `location_lng` (DOUBLE PRECISION, -180 to 180)
   - `date_of_story` (DATE, nullable)
   - `created_at`, `updated_at` (TIMESTAMPTZ)

3. **photos**
   - `id` (UUID, primary key)
   - `story_id` (UUID, FK → stories.id, ON DELETE CASCADE)
   - `gcs_url` (TEXT, not null)
   - `filename` (TEXT, nullable)
   - `caption` (TEXT, nullable)
   - `ordinal` (INT, default 0)
   - `created_at` (TIMESTAMPTZ)

### Indexes
- `idx_users_email` - Partial index on email (WHERE email IS NOT NULL)
- `idx_stories_owner_id` - FK index
- `idx_stories_created_at` - Descending, for timeline queries
- `idx_stories_category_created_at` - Composite, for filtered timelines
- `idx_photos_story_id` - FK index
- `idx_photos_story_id_ordinal` - Composite, for ordered photo retrieval

### Triggers
- `update_stories_updated_at` - Auto-updates `stories.updated_at` on modification

## Common Commands

```bash
# Check current database revision
alembic -c alembic.ini current

# View migration history
alembic -c alembic.ini history

# Apply all pending migrations
alembic -c alembic.ini upgrade head

# Rollback one migration
alembic -c alembic.ini downgrade -1

# Rollback all migrations
alembic -c alembic.ini downgrade base

# Create a new migration (manual)
alembic -c alembic.ini revision -m "description"

# Generate migration from model changes (requires models)
alembic -c alembic.ini revision --autogenerate -m "description"
```

## Verification

After running migrations, verify with:

```sql
-- Check tables were created
\dt

-- Check the stories table structure
\d stories

-- Verify alembic tracking
SELECT * FROM alembic_version;
```

Expected output from `alembic current`:
```
20260125_120000 (head)
```

## Troubleshooting

### Error: "DATABASE_URL environment variable is not set"
- Ensure `.env` file exists in `backend/` directory
- Check that `DATABASE_URL` is set correctly in `.env`
- Format: `postgresql://username:password@host:port/database`

### Error: "could not connect to server"
- Verify PostgreSQL is running
- Check host/port in DATABASE_URL
- Ensure database exists: `createdb geostory`

### Error: "permission denied"
- Ensure database user has CREATE privileges
- Grant permissions: `GRANT ALL PRIVILEGES ON DATABASE geostory TO ls_user;`

### Error: "alembic command not found"
- Install Alembic: `pip install alembic`
- Or reinstall all dependencies: `pip install -r requirements.txt`

## Next Steps

1. ✅ Migrations are set up and documented
2. ⏭️ Create SQLAlchemy ORM models in `backend/app/models/`
3. ⏭️ Implement database connection and session management
4. ⏭️ Add story CRUD endpoints
5. ⏭️ Implement photo upload to Google Cloud Storage

## Notes

- Migrations use **synchronous** SQLAlchemy connections (standard for DDL)
- The application can use async drivers (e.g., `asyncpg`) separately
- Always test migrations on a development database first
- The initial migration matches `docs/schema.sql` exactly
- Schema design documented in `docs/schema.md`
