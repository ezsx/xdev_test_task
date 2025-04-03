from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Create an async engine for PostgreSQL
engine = create_async_engine(
    settings.postgres_db_url,
    echo=False,  # settings.sql_echo,  # Shows SQL queries in logs; consider disabling in production.
)

# Create a session factory
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Dependency for retrieving an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
