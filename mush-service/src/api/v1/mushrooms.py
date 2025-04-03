from uuid import UUID

from fastapi import APIRouter, Depends, status
from schemas.mushroom import MushroomCreate, MushroomResponse, MushroomUpdate
from services.mushroom_service import MushroomService, get_mushroom_service

router = APIRouter()


@router.post(
    "/",
    response_model=MushroomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание гриба",
    description="Создает новый гриб с указанными характеристиками.",
)
async def create_mushroom(
    mushroom_data: MushroomCreate,
    service: MushroomService = Depends(get_mushroom_service),
) -> MushroomResponse:
    return await service.create_mushroom(mushroom_data)


@router.put(
    "/{mushroom_id}",
    response_model=MushroomResponse,
    summary="Обновление гриба",
    description="Обновляет данные гриба по его идентификатору.",
)
async def update_mushroom(
    mushroom_id: UUID,
    update_data: MushroomUpdate,
    service: MushroomService = Depends(get_mushroom_service),
) -> MushroomResponse:
    return await service.update_mushroom(mushroom_id, update_data)


@router.get(
    "/{mushroom_id}",
    response_model=MushroomResponse,
    summary="Получение гриба",
    description="Возвращает данные гриба по его идентификатору с использованием кэша.",
)
async def get_mushroom(
    mushroom_id: UUID, service: MushroomService = Depends(get_mushroom_service)
) -> MushroomResponse:
    return await service.get_mushroom(mushroom_id)
