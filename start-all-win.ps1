# Запуск основных сервисов
Write-Host "Запуск основных сервисов... для теста"
docker compose -f docker-compose-mush.yml --profile pytest up -d --build
Start-Sleep -Seconds 3

# Установка переменной окружения PYTHONPATH
$env:PYTHONPATH = $PWD
Write-Host "Установлен PYTHONPATH: $env:PYTHONPATH"
