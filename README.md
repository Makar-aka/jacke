# Простой генератор пароля.
```
git clone https://github.com/Makar-aka/jacke.git && cd jacke
```
## Создайте .env
```
TELEGRAM_TOKEN=токен
ALLOWED_USERS=123456,1234121 #id админов через запятую.
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
PASSWORD_LENGTH=10
```
```
pip3 install -r requirements.txt
```
Запуск -
```
python3 jacke.py
```
------------
## Для запуска в docker compose


### Создайте docker-compose.yml

```
services:
  jacke-app:
    build: https://github.com/Makar-aka/jacke.git
    command: python jacke.py
    volumes:
      - ./logs:/app/logs
      - ./.env:/app/.env
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - ALLOWED_USERS=${ALLOWED_USERS}
      - LOG_LEVEL=${LOG_LEVEL}
      - LOG_FILE=/app/logs/bot.log
      - PASSWORD_LENGTH=${PASSWORD_LENGTH}
    restart: unless-stopped
```
```
mkdir logs
```
```
touch logs/bot.log
```

```
docker compose up -d
```
