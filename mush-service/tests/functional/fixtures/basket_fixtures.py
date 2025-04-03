# tests/functional/fixtures/basket_fixtures.py
import pytest
from httpx import AsyncClient


@pytest.fixture
def create_basket(base_url):
    """
    Фикстура, возвращающая асинхронную функцию для создания корзинки через POST /basket/.
    """

    async def _create_basket(owner: str = "Иван", capacity: int = 1000) -> str:
        data = {"owner": owner, "capacity": capacity}
        async with AsyncClient() as client:
            response = await client.post(f"{base_url}/basket/", json=data)
            assert response.status_code == 201, f"Create basket failed: {response.text}"
            return response.json()["id"]

    return _create_basket


@pytest.fixture
def add_mushroom_to_basket(base_url):
    """
    Функция для добавления гриба в корзинку через POST /basket/{basket_id}/mushrooms.
    """

    async def _add_mushroom_to_basket(basket_id: str, mushroom_id: str):
        async with AsyncClient() as client:
            url = f"{base_url}/basket/{basket_id}/mushrooms"
            # здесь без слэша на конце, т.к. конкретно у вас маршрут @router.post("/{basket_id}/mushrooms")
            params = {"mushroom_id": mushroom_id}
            return await client.post(url, params=params)

    return _add_mushroom_to_basket


@pytest.fixture
def remove_mushroom_from_basket(base_url):
    """
    Удаление гриба из корзинки: DELETE /basket/{basket_id}/mushrooms/{mushroom_id}
    """

    async def _remove_mushroom_from_basket(basket_id: str, mushroom_id: str):
        async with AsyncClient() as client:
            url = f"{base_url}/basket/{basket_id}/mushrooms/{mushroom_id}"
            return await client.delete(url)

    return _remove_mushroom_from_basket
