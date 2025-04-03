# tests/functional/src/test_mush.py
import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.mark.describe("Mushrooms API")
class TestMushrooms:
    @pytest.mark.it("Успешное создание гриба")
    async def test_create_mushroom_success(self, base_url):
        new_mushroom = {"name": "Лисичка", "edible": True, "weight": 80, "fresh": True}
        async with AsyncClient() as client:
            response = await client.post(f"{base_url}/mush/", json=new_mushroom)
            assert response.status_code == 201, f"Create failed: {response.text}"

            body = response.json()
            assert "id" in body, "Response must contain mushroom id"
            assert body["name"] == new_mushroom["name"]
            assert body["edible"] == new_mushroom["edible"]
            assert body["weight"] == new_mushroom["weight"]
            assert body["fresh"] == new_mushroom["fresh"]

    @pytest.mark.it("Невалидное создание гриба (без name)")
    async def test_create_mushroom_invalid(self, base_url):
        invalid_data = {
            # пропускаем "name", чтобы вызвать 422
            "edible": True,
            "weight": 50,
            "fresh": True,
        }
        async with AsyncClient() as client:
            response = await client.post(f"{base_url}/mush/", json=invalid_data)
            assert (
                response.status_code == 422
            ), f"Expected 422, got {response.status_code}"

    @pytest.mark.it("Успешное обновление гриба")
    async def test_update_mushroom_success(self, create_mushroom, base_url):
        # Сначала создаём гриб
        mushroom_id = await create_mushroom(name="Подберёзовик", weight=100)

        # Затем обновляем его
        update_data = {
            "name": "Подберёзовик-обновлённый",
            "weight": 120,
            "fresh": False,
        }

        async with AsyncClient() as client:
            put_resp = await client.put(
                f"{base_url}/mush/{mushroom_id}", json=update_data
            )
            assert put_resp.status_code == 200, put_resp.text
            updated_mush = put_resp.json()
            assert updated_mush["name"] == update_data["name"]
            assert updated_mush["weight"] == update_data["weight"]
            assert updated_mush["fresh"] == update_data["fresh"]

    @pytest.mark.it("Обновление несуществующего гриба")
    async def test_update_mushroom_not_found(self, base_url):
        random_id = str(uuid.uuid4())
        update_data = {"name": "Новый гриб", "weight": 50, "fresh": True}
        async with AsyncClient() as client:
            response = await client.put(
                f"{base_url}/mush/{random_id}", json=update_data
            )
            assert (
                response.status_code == 404
            ), f"Expected 404, got {response.status_code}"

    @pytest.mark.it("Получение гриба по id")
    async def test_get_mushroom_success(self, create_mushroom, base_url):
        # создаём гриб
        mushroom_id = await create_mushroom(name="Опёнок", edible=False)

        async with AsyncClient() as client:
            response = await client.get(f"{base_url}/mush/{mushroom_id}")
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["id"] == mushroom_id
            assert data["name"] == "Опёнок"

    @pytest.mark.it("Получение несуществующего гриба")
    async def test_get_mushroom_not_found(self, base_url):
        random_id = str(uuid.uuid4())
        async with AsyncClient() as client:
            response = await client.get(f"{base_url}/mush/{random_id}")
            assert (
                response.status_code == 404
            ), f"Expected 404, got {response.status_code}"
