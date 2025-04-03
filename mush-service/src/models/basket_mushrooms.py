from db.models_base import Base
from sqlalchemy import Column, ForeignKey, Table

basket_mushrooms = Table(
    "basket_mushrooms",
    Base.metadata,
    Column("basket_id", ForeignKey("baskets.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "mushroom_id", ForeignKey("mushrooms.id", ondelete="CASCADE"), primary_key=True
    ),
)
