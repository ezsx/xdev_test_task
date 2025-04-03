import uuid

from db.models_base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Basket(Base):
    """
    Модель, представляющая корзинку.

    Обязательные поля:
      - id: UUID
      - owner: имя владельца корзинки
      - capacity: вместительность в граммах
      - mushrooms: список грибов, добавленных в корзинку
    """

    __tablename__ = "baskets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)  # вместительность в граммах

    mushrooms = relationship(
        "Mushroom", secondary="basket_mushrooms", back_populates="baskets"
    )
