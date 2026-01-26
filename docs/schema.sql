-- GeoStory Database Schema
-- PostgreSQL 14+
-- Version: 1.0 (MVP)
-- 
-- This script creates the initial database schema for GeoStory.
-- Run on a fresh database with appropriate permissions.
--
-- Usage:
--   psql -U postgres -d geostory < schema.sql

-- ============================================================================
-- EXTENSIONS
-- ============================================================================

-- Enable pgcrypto for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================================
-- TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- users: Minimal user entity for optional authentication
-- ----------------------------------------------------------------------------
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE,  -- Nullable to support anonymous stories
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email) WHERE email IS NOT NULL;

-- Comments
COMMENT ON TABLE users IS 'User accounts. Email is nullable to support anonymous story creation.';
COMMENT ON COLUMN users.email IS 'User email address. Null for anonymous users.';

-- ----------------------------------------------------------------------------
-- stories: Core location-based story entity
-- ----------------------------------------------------------------------------
CREATE TABLE stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES users(id) ON DELETE SET NULL,  -- Nullable for anonymous stories
    title TEXT NOT NULL,
    body TEXT,
    category TEXT CHECK (category IN (
        'travel',
        'food',
        'history',
        'culture',
        'nature',
        'urban',
        'personal'
    )),
    location_lat DOUBLE PRECISION NOT NULL 
        CHECK (location_lat >= -90 AND location_lat <= 90),
    location_lng DOUBLE PRECISION NOT NULL 
        CHECK (location_lng >= -180 AND location_lng <= 180),
    date_of_story DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX idx_stories_owner_id ON stories(owner_id);
CREATE INDEX idx_stories_created_at ON stories(created_at DESC);
CREATE INDEX idx_stories_category_created_at ON stories(category, created_at DESC);

-- Comments
COMMENT ON TABLE stories IS 'Location-based stories created by users or anonymously.';
COMMENT ON COLUMN stories.owner_id IS 'User who created the story. Null for anonymous stories.';
COMMENT ON COLUMN stories.category IS 'Story category from predefined list.';
COMMENT ON COLUMN stories.location_lat IS 'Latitude in WGS84 decimal degrees (-90 to 90).';
COMMENT ON COLUMN stories.location_lng IS 'Longitude in WGS84 decimal degrees (-180 to 180).';
COMMENT ON COLUMN stories.date_of_story IS 'Date when the story event occurred (may differ from created_at).';

-- ----------------------------------------------------------------------------
-- photos: Photo metadata for stories (images stored in GCS)
-- ----------------------------------------------------------------------------
CREATE TABLE photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    gcs_url TEXT NOT NULL,  -- Google Cloud Storage URL
    filename TEXT,
    caption TEXT,
    ordinal INT NOT NULL DEFAULT 0,  -- Display order (0-indexed)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX idx_photos_story_id ON photos(story_id);
CREATE INDEX idx_photos_story_id_ordinal ON photos(story_id, ordinal);

-- Comments
COMMENT ON TABLE photos IS 'Photo metadata for stories. Actual images stored in Google Cloud Storage.';
COMMENT ON COLUMN photos.gcs_url IS 'Full URL to image in Google Cloud Storage.';
COMMENT ON COLUMN photos.ordinal IS 'Display order for story gallery (0 = first photo).';

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Auto-update stories.updated_at on modification
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_stories_updated_at 
    BEFORE UPDATE ON stories
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON FUNCTION update_updated_at_column() IS 'Automatically updates updated_at timestamp on row modification.';

-- ============================================================================
-- SAMPLE DATA (Optional - for development/testing)
-- ============================================================================

-- Uncomment to insert sample data

-- INSERT INTO users (email) VALUES
--     ('alice@example.com'),
--     ('bob@example.com');

-- INSERT INTO stories (owner_id, title, body, category, location_lat, location_lng, date_of_story) VALUES
--     (
--         (SELECT id FROM users WHERE email = 'alice@example.com'),
--         'Golden Gate Bridge at Sunset',
--         'Caught the most amazing sunset today. The fog was rolling in just as the sun dipped below the horizon.',
--         'travel',
--         37.8199,
--         -122.4783,
--         '2026-01-20'
--     ),
--     (
--         NULL,  -- Anonymous story
--         'Best Pizza in Naples',
--         'Found this tiny pizzeria in the historic district. Life-changing margherita.',
--         'food',
--         40.8518,
--         14.2681,
--         '2025-12-15'
--     );

-- INSERT INTO photos (story_id, gcs_url, filename, ordinal) VALUES
--     (
--         (SELECT id FROM stories WHERE title = 'Golden Gate Bridge at Sunset'),
--         'https://storage.googleapis.com/geostory-uploads/golden-gate-sunset-1.jpg',
--         'golden-gate-sunset-1.jpg',
--         0
--     );

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check table creation
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Check constraints
-- SELECT conname, contype FROM pg_constraint WHERE conrelid = 'stories'::regclass;

-- Check indexes
-- SELECT indexname FROM pg_indexes WHERE schemaname = 'public';
