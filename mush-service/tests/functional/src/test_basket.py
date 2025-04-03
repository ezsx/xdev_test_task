# tests/functional/src/test_basket.py
import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.mark.describe("Basket API")
class TestBasket:
    @pytest.mark.it("Успешное создание корзинки")
    async def test_create_basket_success(self, base_url):
        basket_data = {"owner": "Пётр", "capacity": 500}
        async with AsyncClient() as client:
            resp = await client.post(f"{base_url}/basket/", json=basket_data)
            assert resp.status_code == 201, resp.text
            created_basket = resp.json()
            assert "id" in created_basket
            assert created_basket["owner"] == "Пётр"
            assert created_basket["capacity"] == 500

    @pytest.mark.it("Невалидное создание корзинки (без owner)")
    async def test_create_basket_invalid(self, base_url):
        invalid_data = {"capacity": 300}
        async with AsyncClient() as client:
            resp = await client.post(f"{base_url}/basket/", json=invalid_data)
            assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"

    @pytest.mark.it("Добавление гриба в корзинку")
    async def test_add_mushroom_to_basket(
        self, create_basket, create_mushroom, base_url
    ):
        # Создаём корзинку и гриб
        basket_id = await create_basket(owner="Иван", capacity=200)
        mushroom_id = await create_mushroom(name="Шампиньон", weight=50)

        # Добавляем гриб в корзинку
        async with AsyncClient() as client:
            url = f"{base_url}/basket/{basket_id}/mushrooms"
            params = {"mushroom_id": mushroom_id}
            add_resp = await client.post(url, params=params)
            assert add_resp.status_code == 200, add_resp.text

            # Проверяем, что гриб отобразился внутри корзинки
            updated_basket = add_resp.json()
            mushrooms_list = updated_basket["mushrooms"]
            assert len(mushrooms_list) == 1
            assert mushrooms_list[0]["id"] == mushroom_id

    @pytest.mark.it("Добавление гриба, которого не существует")
    async def test_add_nonexistent_mushroom(self, create_basket, base_url):
        basket_id = await create_basket(owner="Иван")
        fake_mushroom_id = str(uuid.uuid4())

        async with AsyncClient() as client:
            url = f"{base_url}/basket/{basket_id}/mushrooms"
            params = {"mushroom_id": fake_mushroom_id}
            resp = await client.post(url, params=params)
            assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"

    @pytest.mark.it("Превышение вместимости корзинки")
    async def test_add_mushroom_exceeds_capacity(
        self, create_basket, create_mushroom, base_url
    ):
        basket_id = await create_basket(owner="Егор", capacity=50)
        big_mushroom_id = await create_mushroom(
            name="Гигант", weight=100
        )  # вес 100 > capacity=50

        async with AsyncClient() as client:
            url = f"{base_url}/basket/{basket_id}/mushrooms"
            params = {"mushroom_id": big_mushroom_id}
            resp = await client.post(url, params=params)
            # Предположим, что сервис возвращает 400 при превышении вместимости
            assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"

    @pytest.mark.it("Удаление гриба из корзинки")
    async def test_remove_mushroom_from_basket(
        self, create_basket, create_mushroom, base_url
    ):
        # Создаём корзинку и гриб
        basket_id = await create_basket(capacity=200)
        mush_id = await create_mushroom(weight=50)

        # Сначала добавляем
        async with AsyncClient() as client:
            add_url = f"{base_url}/basket/{basket_id}/mushrooms"
            add_resp = await client.post(add_url, params={"mushroom_id": mush_id})
            assert add_resp.status_code == 200, add_resp.text

            # Удаляем
            remove_url = f"{base_url}/basket/{basket_id}/mushrooms/{mush_id}"
            del_resp = await client.delete(remove_url)
            assert del_resp.status_code == 200, del_resp.text

            # Проверяем, что в корзинке больше нет гриба
            updated_basket = del_resp.json()
            assert not updated_basket["mushrooms"], "Basket must be empty"

    @pytest.mark.it("Удаление несуществующего гриба")
    async def test_remove_nonexistent_mushroom(self, create_basket, base_url):
        basket_id = await create_basket(capacity=200)
        fake_mushroom_id = str(uuid.uuid4())

        async with AsyncClient() as client:
            remove_url = f"{base_url}/basket/{basket_id}/mushrooms/{fake_mushroom_id}"
            del_resp = await client.delete(remove_url)
            # Предположим, что сервис возвращает 404, если такого гриба нет в корзинке
            assert (
                del_resp.status_code == 404
            ), f"Expected 404, got {del_resp.status_code}"

    @pytest.mark.it("Получение корзинки")
    async def test_get_basket_success(self, create_basket, base_url):
        # Создадим корзинку
        basket_id = await create_basket(owner="Сергей", capacity=300)

        async with AsyncClient() as client:
            get_resp = await client.get(f"{base_url}/basket/{basket_id}")
            assert get_resp.status_code == 200, get_resp.text
            basket_data = get_resp.json()
            assert basket_data["id"] == basket_id
            assert basket_data["owner"] == "Сергей"
            assert basket_data["capacity"] == 300

    @pytest.mark.it("Получение несуществующей корзинки")
    async def test_get_basket_not_found(self, base_url):
        fake_id = str(uuid.uuid4())
        async with AsyncClient() as client:
            resp = await client.get(f"{base_url}/basket/{fake_id}")
            assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
