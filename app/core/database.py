from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings

engine = create_async_engine(
    settings.DATABASE_URL,  # Already has postgresql+asyncpg://
    pool_size=10,
    max_overflow=100
)

# Preferred SQLAlchemy 2.0 factory for async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session