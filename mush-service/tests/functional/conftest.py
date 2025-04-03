# tests/functional/conftest.py
import pytest

# Подключаем наши фикстуры (папка fixtures)
pytest_plugins = [
    "fixtures.basket_fixtures",
    "fixtures.mush_fixtures",
]


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Базовый URL для запросов.
    В реальном проекте это может быть http://localhost:8000, либо
    использоваться динамическая адресация при поднятии docker-compose.
    """
    return "http://mush-fastapi:8000/store"
