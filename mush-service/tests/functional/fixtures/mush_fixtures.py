# tests/functional/fixtures/mush_fixtures.py
import pytest
from httpx import AsyncClient


@pytest.fixture
def create_mushroom(base_url):
    """
    Фикстура, возвращающая асинхронную функцию для создания гриба через POST /mush/.
    """

    async def _create_mushroom(
        name: str = "Белый гриб",
        edible: bool = True,
        weight: int = 100,
        fresh: bool = True,
    ) -> str:
        data = {"name": name, "edible": edible, "weight": weight, "fresh": fresh}
        async with AsyncClient() as client:
            response = await client.post(f"{base_url}/mush/", json=data)
            assert (
                response.status_code == 201
            ), f"Create mushroom failed: {response.text}"
            return response.json()["id"]

    return _create_mushroom
