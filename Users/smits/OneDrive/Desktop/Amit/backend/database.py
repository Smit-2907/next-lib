from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Database configuration: defaults to SQLite, but can be overridden by environment variable
# SQLite URL: sqlite+aiosqlite:///./library.db
# MySQL URL (example): mysql+aiomysql://root:password@localhost/library_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./library.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
