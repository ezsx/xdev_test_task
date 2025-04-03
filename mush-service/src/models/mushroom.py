import uuid

from db.models_base import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Mushroom(Base):
    """
    Модель, представляющая гриб.

    Обязательные поля:
      - id: UUID
      - name: название гриба
      - edible: съедобность (True - съедобный, False - ядовитый)
      - weight: вес в граммах
      - fresh: свежесть (True - свежий, False - не свежий)
    """

    __tablename__ = "mushrooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    edible = Column(Boolean, nullable=False)
    weight = Column(Integer, nullable=False)  # вес в граммах
    fresh = Column(Boolean, nullable=False)

    baskets = relationship(
        "Basket", secondary="basket_mushrooms", back_populates="mushrooms"
    )
