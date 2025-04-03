#!/bin/bash

# Если не одна миграция еще не создана:
# echo "Initializing Alembic migrations if not present..."
# alembic revision --autogenerate -m "Initial migration"


# Применяем все миграции
echo "Applying database migrations..."
alembic upgrade head

# Запуск приложения
echo "Starting FastAPI application..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000

# Для дебагинга внутри контейнера:
echo "Sleep start ..."
sleep 30d
