"""Application configuration using Pydantic settings.

This module provides centralized configuration management for the GeoStory backend.
Settings are loaded from environment variables and .env files.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    All settings can be configured via environment variables or a .env file.
    """
    
    # Database configuration
    # Format: postgresql+asyncpg://user:password@host:port/database
    # Example: postgresql+asyncpg://ls_user:password@localhost:5432/geostory
    DATABASE_URL: str = "postgresql+asyncpg://ls_user:password@localhost:5432/geostory"
    
    # CORS configuration
    # Comma-separated list of allowed origins
    # Example: http://localhost:5173,http://localhost:3000
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Application environment
    APP_ENV: str = "development"
    
    # Debug mode
    DEBUG: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list of origins."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
# Import this in other modules to access configuration
settings = Settings()
