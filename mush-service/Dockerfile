# Используем Python 3.11 в качестве базового образа
FROM python:3.11-slim

# # Создаем пользователя и группу для безопасного запуска
# RUN groupadd -g 1001 web && useradd -u 1001 -g web web

# # Устанавливаем пользователя для безопасности
# USER 1001:1001

# Устанавливаем рабочую директорию
WORKDIR /opt/app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /opt/app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы
COPY . /opt/app

# Устанавливаем права на скрипт entry-point.sh и передаем права пользователю web
# COPY entry-point.sh /opt/app/
# RUN chmod +x /opt/app/entry-point.sh \
#     && chown -R web:web /opt/app

# Запуск приложения через скрипт entry-point.sh 
ENTRYPOINT ["/bin/bash", "-c", "source /opt/app/entry-point.sh"]
 