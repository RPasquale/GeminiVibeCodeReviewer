"""
Database setup and connection management.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from loguru import logger

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Metadata for database schema
metadata = MetaData()

async def init_db():
    """Initialize database connection and create tables."""
    try:
        # Test database connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute("SELECT 1"))
        
        logger.info("Database connection established successfully")
        
        # Create tables (if using SQLAlchemy models)
        # async with engine.begin() as conn:
        #     await conn.run_sync(metadata.create_all)
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()

async def close_db():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")
