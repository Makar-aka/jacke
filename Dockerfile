# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем папку для логов и устанавливаем права
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Указываем переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем приложение
CMD ["python", "jacke.py"]
