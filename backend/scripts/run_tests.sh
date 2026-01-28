#!/bin/bash

# Backend Test Runner Script
# This script sets up the test database and runs the full test suite.

set -e  # Exit on any error

echo "🧪 GeoStory Backend Test Runner"
echo "================================"

# Configuration
export TEST_DATABASE_URL="postgresql+asyncpg://geostory_user:geostory_pass@localhost:5433/geostory_test"
export DATABASE_URL="$TEST_DATABASE_URL"  # For alembic migrations

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Start test database
echo ""
echo "${YELLOW}📦 Starting test database...${NC}"
docker-compose -f docker-compose.test.yml up -d

# Step 2: Wait for database to be ready
echo ""
echo "${YELLOW}⏳ Waiting for database to be ready...${NC}"
for i in {1..30}; do
    if docker-compose -f docker-compose.test.yml exec -T db_test pg_isready -U geostory_user -d geostory_test > /dev/null 2>&1; then
        echo "${GREEN}✅ Database is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "${RED}❌ Database failed to start${NC}"
        exit 1
    fi
    echo "  Attempt $i/30..."
    sleep 1
done

# Step 3: Run migrations
echo ""
echo "${YELLOW}🔄 Running database migrations...${NC}"
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "${GREEN}✅ Migrations completed${NC}"
else
    echo "${RED}❌ Migrations failed${NC}"
    exit 1
fi

# Step 4: Run tests
echo ""
echo "${YELLOW}🧪 Running tests...${NC}"
pytest tests/ -v --tb=short --color=yes

TEST_EXIT_CODE=$?

# Step 5: Report results
echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "${GREEN}✅ All tests passed!${NC}"
else
    echo "${RED}❌ Some tests failed${NC}"
fi

# Optional: Cleanup (comment out if you want to keep DB running for debugging)
# echo ""
# echo "${YELLOW}🧹 Cleaning up...${NC}"
# docker-compose -f docker-compose.test.yml down

exit $TEST_EXIT_CODE
