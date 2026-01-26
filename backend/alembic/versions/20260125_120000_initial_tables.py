"""Initial database schema with users, stories, and photos tables.

This migration creates the core GeoStory schema as defined in docs/schema.sql.
It includes:
- pgcrypto extension for UUID generation
- users table for optional authentication
- stories table with location data and constraints
- photos table for story images (stored in GCS)
- All indexes for optimal query performance
- Trigger for auto-updating stories.updated_at

Revision ID: 20260125_120000
Revises: 
Create Date: 2026-01-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260125_120000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database schema."""
    
    # Enable pgcrypto extension for gen_random_uuid()
    # This is safe to run multiple times (IF NOT EXISTS)
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    
    # ========================================================================
    # Create users table
    # ========================================================================
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        comment='User accounts. Email is nullable to support anonymous story creation.'
    )
    
    # Index for email lookups (partial index excluding nulls)
    op.create_index(
        'idx_users_email',
        'users',
        ['email'],
        unique=False,
        postgresql_where=sa.text('email IS NOT NULL')
    )
    
    # ========================================================================
    # Create stories table
    # ========================================================================
    op.create_table(
        'stories',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('owner_id', postgresql.UUID(), nullable=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('category', sa.Text(), nullable=True),
        sa.Column('location_lat', sa.Double(), nullable=False),
        sa.Column('location_lng', sa.Double(), nullable=False),
        sa.Column('date_of_story', sa.Date(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        # Constraints
        sa.CheckConstraint(
            'location_lat >= -90 AND location_lat <= 90',
            name='stories_latitude_check'
        ),
        sa.CheckConstraint(
            'location_lng >= -180 AND location_lng <= 180',
            name='stories_longitude_check'
        ),
        sa.CheckConstraint(
            "category IN ('travel', 'food', 'history', 'culture', 'nature', 'urban', 'personal')",
            name='stories_category_check'
        ),
        sa.ForeignKeyConstraint(
            ['owner_id'],
            ['users.id'],
            ondelete='SET NULL'
        ),
        sa.PrimaryKeyConstraint('id'),
        comment='Location-based stories created by users or anonymously.'
    )
    
    # Indexes for stories table
    op.create_index('idx_stories_owner_id', 'stories', ['owner_id'])
    op.create_index('idx_stories_created_at', 'stories', [sa.text('created_at DESC')])
    op.create_index('idx_stories_category_created_at', 'stories', ['category', sa.text('created_at DESC')])
    
    # ========================================================================
    # Create photos table
    # ========================================================================
    op.create_table(
        'photos',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('story_id', postgresql.UUID(), nullable=False),
        sa.Column('gcs_url', sa.Text(), nullable=False),
        sa.Column('filename', sa.Text(), nullable=True),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('ordinal', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        # Constraints
        sa.ForeignKeyConstraint(
            ['story_id'],
            ['stories.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        comment='Photo metadata for stories. Actual images stored in Google Cloud Storage.'
    )
    
    # Indexes for photos table
    op.create_index('idx_photos_story_id', 'photos', ['story_id'])
    op.create_index('idx_photos_story_id_ordinal', 'photos', ['story_id', 'ordinal'])
    
    # ========================================================================
    # Create trigger function and trigger for stories.updated_at
    # ========================================================================
    
    # Create function to update updated_at timestamp
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Create trigger on stories table
    op.execute("""
        CREATE TRIGGER update_stories_updated_at 
        BEFORE UPDATE ON stories
        FOR EACH ROW 
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Drop all tables and extensions created in upgrade."""
    
    # Drop trigger and function first
    op.execute("DROP TRIGGER IF EXISTS update_stories_updated_at ON stories")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_table('photos')
    op.drop_table('stories')
    op.drop_table('users')
    
    # Note: We don't drop the pgcrypto extension as other schemas might use it
    # If you want to drop it, uncomment the line below:
    # op.execute("DROP EXTENSION IF EXISTS pgcrypto")
