# Используем Python 3.11 в качестве базового образа
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /opt/tests
# Копируем requirements.txt для тестов и устанавливаем зависимости
COPY requirements.txt /opt/tests/requirements.txt
RUN pip install --no-cache-dir -r /opt/tests/requirements.txt

# Копируем тестовые файлы и папки в контейнер
COPY . /opt/tests

# Точка входа для выполнения всех тестов
ENTRYPOINT ["/bin/bash", "-c", "source /opt/tests/entrypoint.sh"]
#CMD ["/bin/bash", "-c", "sleep infinity" ]
