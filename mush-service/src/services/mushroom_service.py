import uuid
from typing import Optional

from db.postgres import get_session
from fastapi import Depends, HTTPException, status
from models.basket import Basket
from models.basket_mushrooms import basket_mushrooms
from models.mushroom import Mushroom
from redis.asyncio import Redis
from schemas.mushroom import MushroomCreate, MushroomResponse, MushroomUpdate
from services.cache import get_cache_service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class MushroomService:
    """
    Service for managing mushroom operations with caching.
    """

    def __init__(self, db: AsyncSession, cache: Redis) -> None:
        self.db = db
        self.cache = cache

    async def create_mushroom(self, mushroom_data: MushroomCreate) -> Mushroom:
        """
        Creates a new mushroom instance.
        """
        new_mushroom = Mushroom(
            name=mushroom_data.name,
            edible=mushroom_data.edible,
            weight=mushroom_data.weight,
            fresh=mushroom_data.fresh,
        )
        self.db.add(new_mushroom)
        try:
            await self.db.commit()
            await self.db.refresh(new_mushroom)
            return new_mushroom
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating mushroom.",
            ) from e

    async def update_mushroom(
        self, mushroom_id: uuid.UUID, update_data: MushroomUpdate
    ) -> Mushroom:
        """
        Updates an existing mushroom and invalidates its cache.
        """
        query = select(Mushroom).where(Mushroom.id == mushroom_id)
        result = await self.db.execute(query)
        mushroom = result.scalar_one_or_none()
        if not mushroom:
            raise HTTPException(status_code=404, detail="Mushroom not found.")

        if update_data.name is not None:
            mushroom.name = update_data.name
        if update_data.edible is not None:
            mushroom.edible = update_data.edible
        if update_data.weight is not None:
            mushroom.weight = update_data.weight
        if update_data.fresh is not None:
            mushroom.fresh = update_data.fresh

        try:
            await self.db.commit()
            await self.db.refresh(mushroom)
            # Invalidate cache for this mushroom
            await self.cache.delete(f"mushroom:{mushroom_id}")
            return mushroom
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error updating mushroom.",
            ) from e

    async def get_mushroom(self, mushroom_id: uuid.UUID) -> MushroomResponse:
        """
        Retrieves a mushroom by id, using cache if available.
        """
        cache_key = f"mushroom:{mushroom_id}"
        cached_value = await self.cache.get(cache_key)
        if cached_value:
            # redis returns bytes; декодируем для pydantic
            if isinstance(cached_value, bytes):
                cached_value = cached_value.decode("utf-8")
            return MushroomResponse.parse_raw(cached_value)

        query = select(Mushroom).where(Mushroom.id == mushroom_id)
        result = await self.db.execute(query)
        mushroom = result.scalar_one_or_none()
        if not mushroom:
            raise HTTPException(status_code=404, detail="Mushroom not found.")

        response_data = MushroomResponse.from_orm(mushroom)
        await self.cache.set(
            cache_key, response_data.json(), ex=3600
        )  # кешируем на 1 час
        return response_data


def get_mushroom_service(
    db: AsyncSession = Depends(get_session),
    cache: Redis = Depends(get_cache_service),
) -> MushroomService:
    """Dependency provider for MushroomService."""
    return MushroomService(db, cache)
