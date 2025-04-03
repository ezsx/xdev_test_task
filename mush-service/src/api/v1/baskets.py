from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from schemas.basket import BasketCreate, BasketResponse
from services.basket_service import BasketService, get_basket_service

router = APIRouter()


@router.post(
    "/",
    response_model=BasketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание корзинки",
    description="Создает новую корзинку с указанными характеристиками.",
)
async def create_basket(
    basket_data: BasketCreate, service: BasketService = Depends(get_basket_service)
) -> BasketResponse:
    return await service.create_basket(basket_data)


@router.post(
    "/{basket_id}/mushrooms",
    response_model=BasketResponse,
    summary="Добавление гриба в корзинку",
    description="Добавляет гриб в указанную корзинку, проверяя вместимость и инвалидацию кэша.",
)
async def add_mushroom_to_basket(
    basket_id: UUID,
    mushroom_id: UUID = Query(
        ..., description="Идентификатор гриба, который нужно добавить"
    ),
    service: BasketService = Depends(get_basket_service),
) -> BasketResponse:
    return await service.add_mushroom_to_basket(basket_id, mushroom_id)


@router.delete(
    "/{basket_id}/mushrooms/{mushroom_id}",
    response_model=BasketResponse,
    summary="Удаление гриба из корзинки",
    description="Удаляет гриб из корзинки по заданным идентификаторам и обновляет кэш.",
)
async def remove_mushroom_from_basket(
    basket_id: UUID,
    mushroom_id: UUID,
    service: BasketService = Depends(get_basket_service),
) -> BasketResponse:
    return await service.remove_mushroom_from_basket(basket_id, mushroom_id)


@router.get(
    "/{basket_id}",
    response_model=BasketResponse,
    summary="Получение корзинки",
    description="Возвращает корзинку вместе с развернутой информацией по грибам с использованием кэша.",
)
async def get_basket(
    basket_id: UUID, service: BasketService = Depends(get_basket_service)
) -> BasketResponse:
    return await service.get_basket(basket_id)
