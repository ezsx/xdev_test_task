# /usr/bin/bash

# echo "create common network"
# docker network create -d bridge common_net


echo "Запуск основных сервисов... для теста"
docker compose -f social-service/docker-compose-app.yml --profile loadtest up -d --build --wait
