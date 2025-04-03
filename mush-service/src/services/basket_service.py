import uuid

from db.postgres import get_session
from fastapi import Depends, HTTPException, status
from models.basket import Basket
from models.basket_mushrooms import basket_mushrooms
from models.mushroom import Mushroom
from redis.asyncio import Redis
from schemas.basket import BasketCreate, BasketResponse
from services.cache import get_cache_service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class BasketService:
    """
    Сервис для работы с корзинками, включающий операции создания,
    добавления/удаления грибов и получения данных с использованием кэширования.
    """

    def __init__(self, db: AsyncSession, cache: Redis) -> None:
        self.db = db
        self.cache = cache

    async def create_basket(self, basket_data: BasketCreate) -> Basket:
        """
        Создает новую корзинку.
        """
        new_basket = Basket(owner=basket_data.owner, capacity=basket_data.capacity)
        self.db.add(new_basket)
        try:
            await self.db.commit()
            await self.db.refresh(new_basket, attribute_names=["mushrooms"])
            new_basket.mushrooms = list(new_basket.mushrooms)
            return new_basket
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при создании корзинки.",
            ) from e

    async def add_mushroom_to_basket(
        self, basket_id: uuid.UUID, mushroom_id: uuid.UUID
    ) -> Basket:
        """
        Добавляет гриб в корзинку и инвалидирует кэш корзинки.
        Предзагрузка грибов выполняется через selectinload.
        """
        # Предзагружаем mushrooms, чтобы избежать lazy loading
        query = (
            select(Basket)
            .options(selectinload(Basket.mushrooms))
            .where(Basket.id == basket_id)
        )
        result = await self.db.execute(query)
        basket = result.scalar_one_or_none()
        if not basket:
            raise HTTPException(status_code=404, detail="Корзинка не найдена.")

        query = select(Mushroom).where(Mushroom.id == mushroom_id)
        result = await self.db.execute(query)
        mushroom = result.scalar_one_or_none()
        if not mushroom:
            raise HTTPException(status_code=404, detail="Гриб не найден.")

        if mushroom in basket.mushrooms:
            raise HTTPException(status_code=400, detail="Гриб уже в корзинке.")

        current_weight = sum(m.weight for m in basket.mushrooms)
        if current_weight + mushroom.weight > basket.capacity:
            raise HTTPException(
                status_code=400,
                detail="Добавление этого гриба превышает вместимость корзинки.",
            )

        basket.mushrooms.append(mushroom)
        try:
            await self.db.commit()
            # Обновляем данные с предзагрузкой mushrooms
            await self.db.refresh(basket, attribute_names=["mushrooms"])
            # Инвалидируем кэш для данной корзинки
            await self.cache.delete(f"basket:{basket_id}")
            return basket
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при добавлении гриба в корзинку.",
            ) from e

    async def remove_mushroom_from_basket(
        self, basket_id: uuid.UUID, mushroom_id: uuid.UUID
    ) -> Basket:
        """
        Удаляет гриб из корзинки и инвалидирует кэш.
        Предзагрузка связи mushrooms для избежания lazy loading.
        """
        query = (
            select(Basket)
            .options(selectinload(Basket.mushrooms))
            .where(Basket.id == basket_id)
        )
        result = await self.db.execute(query)
        basket = result.scalar_one_or_none()
        if not basket:
            raise HTTPException(status_code=404, detail="Корзинка не найдена.")

        mushroom_to_remove = None
        for m in basket.mushrooms:
            if m.id == mushroom_id:
                mushroom_to_remove = m
                break

        if not mushroom_to_remove:
            raise HTTPException(status_code=404, detail="Гриб не найден в корзинке.")

        basket.mushrooms.remove(mushroom_to_remove)
        try:
            await self.db.commit()
            await self.db.refresh(basket, attribute_names=["mushrooms"])
            await self.cache.delete(f"basket:{basket_id}")
            return basket
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при удалении гриба из корзинки.",
            ) from e

    async def get_basket(self, basket_id: uuid.UUID) -> BasketResponse:
        """
        Получает данные корзинки вместе со списком грибов, используя кэширование.
        Предзагрузка mushrooms с помощью selectinload.
        """
        cache_key = f"basket:{basket_id}"
        cached_value = await self.cache.get(cache_key)
        if cached_value:
            if isinstance(cached_value, bytes):
                cached_value = cached_value.decode("utf-8")
            return BasketResponse.parse_raw(cached_value)

        query = (
            select(Basket)
            .options(selectinload(Basket.mushrooms))
            .where(Basket.id == basket_id)
        )
        result = await self.db.execute(query)
        basket = result.scalar_one_or_none()
        if not basket:
            raise HTTPException(status_code=404, detail="Корзинка не найдена.")

        response_data = BasketResponse.from_orm(basket)
        await self.cache.set(
            cache_key, response_data.json(), ex=3600
        )  # Кэширование на 1 час
        return response_data


def get_basket_service(
    db: AsyncSession = Depends(get_session),
    cache: Redis = Depends(get_cache_service),
) -> BasketService:
    """Поставщик зависимости для BasketService."""
    return BasketService(db, cache)
