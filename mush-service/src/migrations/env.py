import asyncio
from logging.config import fileConfig

from alembic import context
from core.config import settings
from db.models_base import Base
from models.basket import Basket
from models.basket_mushrooms import basket_mushrooms
from models.mushroom import Mushroom
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.postgres_db_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        settings.postgres_db_url,
        poolclass=NullPool,
        future=True,
    )

    async def async_run_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(sync_run_migrations)

    asyncio.run(async_run_migrations())


def sync_run_migrations(connection) -> None:
    """Run migrations synchronously."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
