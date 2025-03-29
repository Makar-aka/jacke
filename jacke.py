import random
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
allowed_users = os.getenv("ALLOWED_USERS")
log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "bot.log")

if not token or not allowed_users:
    raise ValueError("Необходимо установить TELEGRAM_TOKEN и ALLOWED_USERS в файле .env")

# Преобразование строки с ID пользователей в список целых чисел
ALLOWED_USERS = list(map(int, allowed_users.split(',')))

# Списки символов для генерации пароля
min_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "x", "z"]
max_letter = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "X", "Z"]
numeral = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
spec = ["*", "-", "_", "+", "?", "%", "~", "#", "$"]

LOGIN = range(1)

def generate_password():
    characters = min_letter + max_letter + numeral + spec
    password = ''.join(random.choice(characters) for _ in range(9))
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

def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("У вас нет доступа к этому боту.")
        return ConversationHandler.END

    update.message.reply_text("Пожалуйста, введите ваш логин:")
    return LOGIN

def login(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("У вас нет доступа к этому боту.")
        return ConversationHandler.END

    login = update.message.text
    password = generate_password()
    
    text = f"Здравствуйте, {escape_html(login)}.\n\nЛогин: <code>{escape_html(login.lower())}</code>\nПароль: <code>{escape_html(password)}</code>"
    
    # Создание кнопки меню
    keyboard = [[KeyboardButton("/start")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(text, parse_mode='HTML', reply_markup=reply_markup)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

def main():
    # Настройка логирования
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Бот запущен")

    request_kwargs = {
        'read_timeout': 20,  # Увеличиваем таймаут чтения до 20 секунд
        'connect_timeout': 10,  # Увеличиваем таймаут соединения до 10 секунд
    }
    
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

if __name__ == '__main__':
    main()


