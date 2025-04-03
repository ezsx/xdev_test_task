# Остановка основных сервисов
echo "Остановка основных сервисов... для теста"
docker compose -f docker-compose-mush.yml --profile pytest down --volumes
