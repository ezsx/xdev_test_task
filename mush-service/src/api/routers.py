from api.v1.baskets import router as baskets_router
from api.v1.mushrooms import router as mushrooms_router
from fastapi import APIRouter

mush_prefix = "/store/mush"
mush_tag = "Mush"

main_router = APIRouter()
main_router.include_router(mushrooms_router, prefix=mush_prefix, tags=[mush_tag])

basket_prefix = "/store/basket"
basket_tag = "Basket"

main_router.include_router(baskets_router, prefix=basket_prefix, tags=[basket_tag])
