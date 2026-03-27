from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Database configuration: defaults to SQLite, but can be overridden by environment variable
# SQLite URL: sqlite+aiosqlite:///./library.db
# MySQL URL (example): mysql+aiomysql://root:password@localhost/library_db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Always put library.db inside the backend folder for consistency
DEFAULT_DB_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'library.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
