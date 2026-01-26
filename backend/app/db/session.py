"""Database session management with async SQLAlchemy.

This module configures the async database engine and session factory
for the application. It provides the async session dependency for
FastAPI endpoints.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


# Create async engine
# Uses asyncpg driver for PostgreSQL
# echo=True in development shows SQL queries in logs
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
# expire_on_commit=False prevents lazy-loading errors after commit
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session.
    
    Yields an AsyncSession that is automatically closed after use.
    Use this as a FastAPI dependency to inject a database session
    into endpoint handlers.
    
    Example:
        @app.get("/stories")
        async def get_stories(db: AsyncSession = Depends(get_async_session)):
            result = await db.execute(select(Story))
            return result.scalars().all()
    
    Yields:
        AsyncSession: An async SQLAlchemy session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
