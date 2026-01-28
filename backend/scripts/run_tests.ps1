# Backend Test Runner Script (PowerShell)
# This script sets up the test database and runs the full test suite.

# Don't stop on stderr output from docker commands (they output warnings to stderr)
$ErrorActionPreference = "Continue"

Write-Host "GeoStory Backend Test Runner" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Configuration
$env:TEST_DATABASE_URL = "postgresql+asyncpg://geostory_user:geostory_pass@localhost:5433/geostory_test"
$env:DATABASE_URL = $env:TEST_DATABASE_URL  # For alembic migrations

# Step 1: Start test database
Write-Host ""
Write-Host "Starting test database..." -ForegroundColor Yellow
docker-compose -f docker-compose.test.yml up -d 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start test database" -ForegroundColor Red
    exit 1
}

# Step 2: Wait for database to be ready
Write-Host ""
Write-Host "Waiting for database to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and -not $ready) {
    $attempt++
    # Use docker exec directly and capture exit code properly
    $null = docker exec geostory_test_db pg_isready -U geostory_user -d geostory_test 2>&1
    if ($LASTEXITCODE -eq 0) {
        $ready = $true
        Write-Host "Database is ready!" -ForegroundColor Green
    } else {
        if ($attempt -eq $maxAttempts) {
            Write-Host "Database failed to start" -ForegroundColor Red
            exit 1
        }
        Write-Host "  Attempt $attempt/$maxAttempts..."
        Start-Sleep -Seconds 1
    }
}

# Step 3: Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
alembic upgrade head

if ($LASTEXITCODE -eq 0) {
    Write-Host "Migrations completed" -ForegroundColor Green
} else {
    Write-Host "Migrations failed" -ForegroundColor Red
    exit 1
}

# Step 4: Run tests
Write-Host ""
Write-Host "Running tests..." -ForegroundColor Yellow
pytest tests/ -v --tb=short --color=yes

$testExitCode = $LASTEXITCODE

# Step 5: Report results
Write-Host ""
if ($testExitCode -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
} else {
    Write-Host "Some tests failed" -ForegroundColor Red
}

# Optional: Cleanup (comment out if you want to keep DB running for debugging)
# Write-Host ""
# Write-Host "Cleaning up..." -ForegroundColor Yellow
# docker-compose -f docker-compose.test.yml down

exit $testExitCode
