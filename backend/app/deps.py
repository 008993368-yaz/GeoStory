"""FastAPI dependency injection utilities.

This module provides reusable dependencies for FastAPI endpoints,
primarily for database session management.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session dependency.
    
    This is the main dependency for database access in FastAPI endpoints.
    It yields an async SQLAlchemy session that is automatically managed.
    
    Usage:
        from app.deps import get_db
        
        @router.get("/stories")
        async def list_stories(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Story))
            return result.scalars().all()
    
    Yields:
        AsyncSession: An async database session
    """
    async for session in get_async_session():
        yield session
