#!/bin/bash
#
# GeoStory Database Migration Runner
#
# This script runs Alembic migrations for the GeoStory database.
# It loads environment variables from .env if present and executes
# 'alembic upgrade head' to apply all pending migrations.
#
# Usage:
#   ./scripts/run_migrations.sh
#
# Requirements:
#   - DATABASE_URL must be set (in .env or as environment variable)
#   - Alembic must be installed (pip install alembic)
#   - PostgreSQL database must be accessible
#
# Example DATABASE_URL:
#   postgresql://ls_user:password@localhost:5432/geostory

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}GeoStory Database Migration Runner${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Change to backend directory (where alembic.ini is located)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BACKEND_DIR"

echo "Working directory: $(pwd)"
echo ""

# Load .env file if it exists
if [ -f .env ]; then
    echo -e "${GREEN}✓${NC} Found .env file, loading environment variables..."
    export $(grep -v '^#' .env | xargs)
else
    echo -e "${YELLOW}⚠${NC} No .env file found, using existing environment variables"
fi
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}✗ ERROR: DATABASE_URL environment variable is not set${NC}"
    echo ""
    echo "Please set DATABASE_URL in one of the following ways:"
    echo "  1. Create a .env file with: DATABASE_URL=postgresql://user:pass@host:port/db"
    echo "  2. Export it: export DATABASE_URL=postgresql://user:pass@host:port/db"
    echo ""
    echo "Example: DATABASE_URL=postgresql://ls_user:password@localhost:5432/geostory"
    exit 1
fi

# Mask password in DATABASE_URL for display
DISPLAY_URL=$(echo "$DATABASE_URL" | sed 's/:\/\/[^:]*:[^@]*@/:\/\/***:***@/')
echo -e "${GREEN}✓${NC} DATABASE_URL is set: $DISPLAY_URL"
echo ""

# Check if alembic command exists
if ! command -v alembic &> /dev/null; then
    echo -e "${RED}✗ ERROR: alembic command not found${NC}"
    echo ""
    echo "Please install Alembic:"
    echo "  pip install alembic"
    exit 1
fi

echo -e "${GREEN}✓${NC} Alembic is installed"
echo ""

# Show current revision before migration
echo "Current database revision:"
alembic -c alembic.ini current || echo "  (no revision - database is empty or uninitialized)"
echo ""

# Run migrations
echo -e "${GREEN}Running migrations...${NC}"
echo "Command: alembic -c alembic.ini upgrade head"
echo ""

if alembic -c alembic.ini upgrade head; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Migrations completed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    # Show current revision after migration
    echo "Current database revision:"
    alembic -c alembic.ini current
    echo ""
    
    exit 0
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ Migration failed${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "Please check the error messages above and verify:"
    echo "  - DATABASE_URL is correct"
    echo "  - PostgreSQL server is running"
    echo "  - Database exists and is accessible"
    echo "  - User has necessary permissions"
    echo ""
    exit 1
fi
