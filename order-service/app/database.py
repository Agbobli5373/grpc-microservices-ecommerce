from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite+aiosqlite:///./data/orders.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)


async def init_db():
    """Initialize the database and create tables"""
    async with engine.begin() as conn:
        # Import all models here to ensure they are registered
        from .models import Order
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Get database session"""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
