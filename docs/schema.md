# GeoStory Database Schema

## Overview

This document describes the PostgreSQL database schema for GeoStory, a location-based visual storytelling platform.

### Design Principles

- **UUIDs for primary keys**: Better for distributed systems, no sequential enumeration, safe for public APIs
- **Temporal tracking**: All entities track creation time; stories track updates
- **Referential integrity**: Foreign keys with explicit cascade behavior
- **Geospatial validation**: Hard constraints on lat/lng ranges
- **Future-ready**: Schema supports evolution to full auth, soft deletes, and full-text search

### Schema Version

Initial schema v1.0 (MVP)

---

## Entity Relationship Diagram (Text)

```
users (1) ----< (0..n) stories
stories (1) ----< (0..n) photos

Relationships:
- A user can own zero or more stories (owner_id is nullable for anonymous stories)
- A story belongs to zero or one user (nullable FK, SET NULL on delete)
- A story has zero or more photos
- A photo belongs to exactly one story (CASCADE on delete)
```

---

## Tables

### `users`

Minimal user entity to support optional authentication. In MVP, stories can be anonymous (owner_id NULL) or attributed to a user.

| Column       | Type         | Constraints                     | Description                          |
|--------------|--------------|---------------------------------|--------------------------------------|
| id           | UUID         | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier          |
| email        | TEXT         | UNIQUE, NULLABLE                | User email (null for anonymous)      |
| created_at   | TIMESTAMPTZ  | NOT NULL, DEFAULT now()         | Account creation timestamp           |

**Indexes:**
- Primary key on `id` (automatic)
- Unique index on `email` (automatic)

**Future considerations:**
- Add `password_hash`, `display_name`, `is_active` when implementing authentication
- Add `updated_at` for audit trails
- Add `role` for permissions (admin, moderator, user)

---

### `stories`

Core entity representing a user's location-based story.

| Column         | Type             | Constraints                                  | Description                              |
|----------------|------------------|----------------------------------------------|------------------------------------------|
| id             | UUID             | PRIMARY KEY, DEFAULT gen_random_uuid()       | Unique story identifier                  |
| owner_id       | UUID             | NULLABLE, FK → users(id) ON DELETE SET NULL  | Story owner (null = anonymous)           |
| title          | TEXT             | NOT NULL                                     | Story title                              |
| body           | TEXT             | NULLABLE                                     | Story content (markdown-friendly)        |
| category       | TEXT             | NULLABLE, CHECK (category IN (...))          | Story category (travel, food, history, etc.) |
| location_lat   | DOUBLE PRECISION | NOT NULL, CHECK (-90 <= location_lat <= 90)  | Latitude (WGS84)                         |
| location_lng   | DOUBLE PRECISION | NOT NULL, CHECK (-180 <= location_lng <= 180)| Longitude (WGS84)                        |
| date_of_story  | DATE             | NULLABLE                                     | When the story event occurred            |
| created_at     | TIMESTAMPTZ      | NOT NULL, DEFAULT now()                      | Record creation timestamp                |
| updated_at     | TIMESTAMPTZ      | NOT NULL, DEFAULT now()                      | Record last update timestamp             |

**Constraints:**
- `stories_latitude_check`: Validates latitude range [-90, 90]
- `stories_longitude_check`: Validates longitude range [-180, 180]
- `stories_category_check`: Limits category to predefined values (see schema.sql)

**Indexes:**
- Primary key on `id` (automatic)
- `idx_stories_created_at`: Supports timeline queries (`ORDER BY created_at DESC`)
- `idx_stories_category_created_at`: Composite index for filtered timelines
- `idx_stories_owner_id`: FK index for user lookups

**Future considerations:**
- Add `is_published BOOLEAN` for draft support
- Add `deleted_at TIMESTAMPTZ` for soft deletes
- Add `search_vector TSVECTOR` with GIN index for full-text search
- Add PostGIS `GEOGRAPHY(Point, 4326)` for advanced spatial queries
- Add `view_count`, `like_count` for engagement metrics

---

### `photos`

Photo metadata for stories. Actual images stored in Google Cloud Storage.

| Column      | Type         | Constraints                                 | Description                           |
|-------------|--------------|---------------------------------------------|---------------------------------------|
| id          | UUID         | PRIMARY KEY, DEFAULT gen_random_uuid()      | Unique photo identifier               |
| story_id    | UUID         | NOT NULL, FK → stories(id) ON DELETE CASCADE| Parent story                          |
| gcs_url     | TEXT         | NOT NULL                                    | Google Cloud Storage URL              |
| filename    | TEXT         | NULLABLE                                    | Original filename                     |
| caption     | TEXT         | NULLABLE                                    | Photo caption/alt text                |
| ordinal     | INT          | NOT NULL, DEFAULT 0                         | Display order (0-indexed)             |
| created_at  | TIMESTAMPTZ  | NOT NULL, DEFAULT now()                     | Upload timestamp                      |

**Constraints:**
- ON DELETE CASCADE: Deleting a story removes all its photos

**Indexes:**
- Primary key on `id` (automatic)
- `idx_photos_story_id`: FK index for story lookups
- `idx_photos_story_id_ordinal`: Composite for ordered retrieval

**Future considerations:**
- Add `width`, `height`, `file_size` for metadata
- Add `blurhash` or `thumbnail_url` for performance
- Add `is_cover BOOLEAN` to mark primary photo
- Add `exif_data JSONB` for camera metadata

---

## Database Extensions

### pgcrypto

Required for `gen_random_uuid()` function.

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

**Future extensions:**
- `postgis`: For advanced geospatial features (proximity search, geometry validation)
- `pg_trgm`: For fuzzy text search
- `uuid-ossp`: Alternative UUID generation (pgcrypto preferred)

---

## Index Strategy

### Current Indexes

| Index Name                         | Table   | Columns               | Purpose                                    |
|------------------------------------|---------|-----------------------|--------------------------------------------|
| stories_pkey                       | stories | id                    | Primary key lookup                         |
| idx_stories_created_at             | stories | created_at DESC       | Timeline queries (newest first)            |
| idx_stories_category_created_at    | stories | category, created_at  | Filtered category timelines                |
| idx_stories_owner_id               | stories | owner_id              | User's stories lookup                      |
| photos_pkey                        | photos  | id                    | Primary key lookup                         |
| idx_photos_story_id                | photos  | story_id              | Story's photos lookup                      |
| idx_photos_story_id_ordinal        | photos  | story_id, ordinal     | Ordered photo retrieval                    |

### Index Rationale

- **created_at DESC**: Most queries display recent stories first
- **category + created_at**: Common filter + sort pattern (e.g., "recent travel stories")
- **story_id + ordinal**: Ensures efficient ordered photo galleries
- **owner_id**: Supports "my stories" user dashboard

### Deferred Indexes

- **Full-text search**: `CREATE INDEX idx_stories_search ON stories USING GIN(to_tsvector('english', title || ' ' || COALESCE(body, '')));`
  - Add when search feature is implemented
  - Consider `pg_trgm` GIN index for fuzzy matching

- **Geospatial proximity**: With PostGIS, add `GIST(geography)` for "stories near me"
  - Current lat/lng columns sufficient for bounding box queries

---

## Data Integrity

### Foreign Keys

- `stories.owner_id → users.id`: ON DELETE SET NULL (preserve anonymous stories if user deleted)
- `photos.story_id → stories.id`: ON DELETE CASCADE (photos belong to story)

### Check Constraints

- **Latitude**: `-90 <= location_lat <= 90`
- **Longitude**: `-180 <= location_lng <= 180`
- **Category**: Limited to valid values (extensible list)

### Uniqueness

- `users.email`: Unique to prevent duplicate accounts (nullable for anonymous support)

---

## Migration Path (Future)

### Phase 1: Authentication (Post-MVP)
- Make `users.email` NOT NULL
- Add `password_hash`, `display_name`, `is_active`
- Create auth tokens table

### Phase 2: Soft Deletes
- Add `deleted_at TIMESTAMPTZ` to stories and photos
- Create partial indexes: `WHERE deleted_at IS NULL`
- Update queries to filter deleted records

### Phase 3: Full-Text Search
- Add `search_vector TSVECTOR` to stories
- Create GIN index
- Set up trigger to auto-update vector on insert/update

### Phase 4: Advanced Geospatial
- Enable PostGIS extension
- Add `geography` column alongside lat/lng
- Create GIST index for proximity searches

### Phase 5: Engagement & Analytics
- Add `view_count`, `like_count` to stories
- Create `story_views` table for detailed analytics
- Add `comments` table for community features

---

## Schema Maintenance

### Update Timestamp Trigger

The schema includes a trigger to automatically update `stories.updated_at` on modifications.

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_stories_updated_at BEFORE UPDATE ON stories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Backup Strategy

- Daily logical backups via `pg_dump`
- Point-in-time recovery enabled (WAL archiving)
- Test restoration quarterly

---

## Performance Considerations

### Expected Query Patterns

1. **List recent stories**: `SELECT * FROM stories WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT 20`
   - Served by `idx_stories_created_at`

2. **Filter by category**: `SELECT * FROM stories WHERE category = 'travel' ORDER BY created_at DESC`
   - Served by `idx_stories_category_created_at`

3. **Story with photos**: `SELECT * FROM photos WHERE story_id = ? ORDER BY ordinal`
   - Served by `idx_photos_story_id_ordinal`

4. **Bounding box search**: `SELECT * FROM stories WHERE location_lat BETWEEN ? AND ? AND location_lng BETWEEN ? AND ?`
   - Sequential scan acceptable for MVP; add GIST index later

### Scaling Notes

- **Read replicas**: Schema supports read-only replicas for timeline queries
- **Partitioning**: Consider partitioning `stories` by `created_at` if table exceeds 10M rows
- **Connection pooling**: Use PgBouncer for high-concurrency scenarios

---

## Security Considerations

### Data Protection

- **No PII in plaintext**: Passwords will be hashed (future)
- **UUIDs prevent enumeration**: No sequential IDs exposed
- **Soft deletes preserve history**: User-deleted content can be audited

### Access Control

- Application-level authorization (not database roles for MVP)
- Future: Row-level security policies for multi-tenant isolation

---

## Appendix: Category Enum

Current valid categories (extensible):
- `travel`
- `food`
- `history`
- `culture`
- `nature`
- `urban`
- `personal`

Implemented as CHECK constraint for flexibility. Consider `ENUM` type if categories become stable.
