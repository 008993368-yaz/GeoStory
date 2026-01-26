# GeoStory Database Migration Runner (PowerShell)
#
# This script runs Alembic migrations for the GeoStory database.
# It loads environment variables from .env if present and executes
# 'alembic upgrade head' to apply all pending migrations.
#
# Usage:
#   .\scripts\run_migrations.ps1
#
# Requirements:
#   - DATABASE_URL must be set (in .env or as environment variable)
#   - Alembic must be installed (pip install alembic)
#   - PostgreSQL database must be accessible
#
# Example DATABASE_URL:
#   postgresql://ls_user:password@localhost:5432/geostory

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "GeoStory Database Migration Runner" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Change to backend directory (where alembic.ini is located)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Split-Path -Parent $ScriptDir
Set-Location $BackendDir

Write-Host "Working directory: $(Get-Location)"
Write-Host ""

# Load .env file if it exists
if (Test-Path .env) {
    Write-Host "[✓] Found .env file, loading environment variables..." -ForegroundColor Green
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)\s*=\s*(.+)\s*$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
} else {
    Write-Host "[⚠] No .env file found, using existing environment variables" -ForegroundColor Yellow
}
Write-Host ""

# Check if DATABASE_URL is set
if (-not $env:DATABASE_URL) {
    Write-Host "[✗] ERROR: DATABASE_URL environment variable is not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set DATABASE_URL in one of the following ways:"
    Write-Host "  1. Create a .env file with: DATABASE_URL=postgresql://user:pass@host:port/db"
    Write-Host "  2. Set it: `$env:DATABASE_URL='postgresql://user:pass@host:port/db'"
    Write-Host ""
    Write-Host "Example: DATABASE_URL=postgresql://ls_user:password@localhost:5432/geostory"
    exit 1
}

# Mask password in DATABASE_URL for display
$DisplayUrl = $env:DATABASE_URL -replace ':\/\/[^:]*:[^@]*@', '://***:***@'
Write-Host "[✓] DATABASE_URL is set: $DisplayUrl" -ForegroundColor Green
Write-Host ""

# Check if alembic command exists
try {
    $null = Get-Command alembic -ErrorAction Stop
    Write-Host "[✓] Alembic is installed" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[✗] ERROR: alembic command not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Alembic:"
    Write-Host "  pip install alembic"
    exit 1
}

# Show current revision before migration
Write-Host "Current database revision:"
try {
    alembic -c alembic.ini current 2>&1
} catch {
    Write-Host "  (no revision - database is empty or uninitialized)"
}
Write-Host ""

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Green
Write-Host "Command: alembic -c alembic.ini upgrade head"
Write-Host ""

try {
    alembic -c alembic.ini upgrade head
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "[✓] Migrations completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Show current revision after migration
    Write-Host "Current database revision:"
    alembic -c alembic.ini current
    Write-Host ""
    
    exit 0
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "[✗] Migration failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the error messages above and verify:"
    Write-Host "  - DATABASE_URL is correct"
    Write-Host "  - PostgreSQL server is running"
    Write-Host "  - Database exists and is accessible"
    Write-Host "  - User has necessary permissions"
    Write-Host ""
    exit 1
}
