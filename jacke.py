import random
import os
import logging
from typing import List, Dict, Any
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv

# Константы
PASSWORD_LENGTH = 9
LOGIN = range(1)

# Настройка логирования
def setup_logging(log_level: str, log_file: str) -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Генерация пароля
def generate_password(length: int = PASSWORD_LENGTH) -> str:
    min_letter = list("abcdefghijklmnopqrstuvwxyz")
    max_letter = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numeral = list("0123456789")
    spec = list("*-_+?%~#$")
    
    characters = min_letter + max_letter + numeral + spec
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def escape_html(text: str) -> str:
    escape_chars = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    return ''.join(escape_chars.get(char, char) for char in text)

def start(update: Update, context: Any) -> int:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("У вас нет доступа к этому боту.")
        return ConversationHandler.END

    update.message.reply_text("Есть че?")
    return LOGIN

def login(update: Update, context: Any) -> int:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("У вас нет доступа к этому боту.")
        return ConversationHandler.END

    login_text = update.message.text
    password = generate_password()
    
    text = (f"Здравствуйте.\n"
            f"Логин: <code>{escape_html(login_text.lower())}</code>\n"
            f"Пароль: <code>{escape_html(password)}</code>")
    
    update.message.reply_text(text, parse_mode='HTML')
    return ConversationHandler.END

def cancel(update: Update, context: Any) -> int:
    update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

def main():
    # Загрузка переменных окружения
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    allowed_users = os.getenv("ALLOWED_USERS")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "bot.log")

    if not token or not allowed_users:
        raise ValueError("Необходимо установить TELEGRAM_TOKEN и ALLOWED_USERS в файле .env")

    # Преобразование строки с ID пользователей в список целых чисел
    global ALLOWED_USERS
    ALLOWED_USERS = list(map(int, allowed_users.split(',')))
    
    # Настройка логирования
    logger = setup_logging(log_level, log_file)
    logger.info("Бот запущен")
    
    request_kwargs = {
        'read_timeout': 20,
        'connect_timeout': 10,
    }
    
    try:
        updater = Updater(token, request_kwargs=request_kwargs)
        dispatcher = updater.dispatcher
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                LOGIN: [MessageHandler(Filters.text & ~Filters.command, login)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        
        dispatcher.add_handler(conv_handler)
        
        updater.start_polling()
        updater.idle()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()
