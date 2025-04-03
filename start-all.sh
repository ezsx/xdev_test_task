# /usr/bin/bash

echo "Запуск основных сервисов... для теста"
docker compose -f docker-compose-mush.yml --profile pytest up -d --build