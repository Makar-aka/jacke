# Базовый образ Python
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY jacke.py .
COPY .env .
# Команда запуска
CMD "python", "jacke.py"
