# tests/functional/src/test_scenario.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.mark.describe("End-to-end scenario")
class TestScenario:
    @pytest.mark.it(
        "Создать гриб, корзинку, добавить гриб в корзинку, удалить гриб и проверить результат"
    )
    async def test_full_scenario(self, create_mushroom, create_basket, base_url):
        # 1) Создать гриб
        mushroom_id = await create_mushroom(name="Груздь", weight=30)

        # 2) Создать корзинку
        basket_id = await create_basket(owner="Анна", capacity=100)

        # 3) Добавить гриб в корзинку
        async with AsyncClient() as client:
            add_url = f"{base_url}/basket/{basket_id}/mushrooms"
            add_resp = await client.post(add_url, params={"mushroom_id": mushroom_id})
            assert add_resp.status_code == 200, add_resp.text
            data = add_resp.json()
            assert len(data["mushrooms"]) == 1

        # 4) Удалить гриб из корзинки
        async with AsyncClient() as client:
            remove_url = f"{base_url}/basket/{basket_id}/mushrooms/{mushroom_id}"
            del_resp = await client.delete(remove_url)
            assert del_resp.status_code == 200, del_resp.text
            updated_basket = del_resp.json()
            assert (
                updated_basket["mushrooms"] == []
            ), "В корзинке не должно остаться грибов"
