from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class MushroomBase(BaseModel):
    name: str
    edible: bool
    weight: int  # вес в граммах
    fresh: bool


class MushroomCreate(MushroomBase):
    """
    Схема для создания гриба.
    Все поля обязательны.
    """

    pass


class MushroomUpdate(BaseModel):
    """
    Схема для обновления гриба.
    Поля опциональные — указываем только те, что нужно обновить.
    """

    name: Optional[str] = None
    edible: Optional[bool] = None
    weight: Optional[int] = None
    fresh: Optional[bool] = None


class MushroomResponse(MushroomBase):
    """
    Схема для возврата данных о грибе.
    Включает идентификатор, сгенерированный БД.
    """

    id: UUID

    class Config:
        from_attributes = True
        orm_mode = True
