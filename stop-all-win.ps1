# Остановка основных сервисов
Write-Host "Остановка основных сервисов... для теста"
docker compose -f docker-compose-mush.yml --profile pytest down --volumes
Start-Sleep -Seconds 2

