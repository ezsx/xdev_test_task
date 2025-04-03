from typing import List
from uuid import UUID

from pydantic import BaseModel
from schemas.mushroom import MushroomResponse


class BasketBase(BaseModel):
    owner: str  # имя владельца корзинки
    capacity: int  # вместимость в граммах


class BasketCreate(BasketBase):
    """
    Схема для создания корзинки.
    """

    pass


class BasketResponse(BasketBase):
    """
    Схема для возврата данных о корзинке.
    Включает идентификатор и список грибов.
    """

    id: UUID
    mushrooms: List[MushroomResponse] = []

    class Config:
        from_attributes = True
        orm_mode = True
