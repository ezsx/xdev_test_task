#!/bin/bash

echo "Запуск основных сервисов... для теста"
docker compose -f docker-compose-mush.yml --profile pytest up -d --build

sleep 3

# Установка переменной окружения PYTHONPATH на текущую директорию
export PYTHONPATH=$(pwd)
echo "Установлен PYTHONPATH: $PYTHONPATH"
