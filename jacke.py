    import random
    import os
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
    from dotenv import load_dotenv

    # Загрузка переменных окружения из файла .env
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")

    # Списки символов для генерации пароля
    min_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "x", "z"]
    max_letter = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "Y", "X", "Z"]
    numeral = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    spec = ["*", "-", "_", "+", "?", "%", "~", "#", "$"]

    LOGIN = range(1)

    def generate_password():
        min_letter_random = random.choice(min_letter)
        min_letter_random_two = random.choice(min_letter)
        max_letter_random = random.choice(max_letter)
        max_letter_random_two = random.choice(max_letter)
        numeral_random = random.choice(numeral)
        numeral_random_two = random.choice(numeral)
        spec_random = random.choice(spec)
        spec_random_two = random.choice(spec)
        
        password = min_letter_random + max_letter_random + numeral_random + spec_random + min_letter_random_two + max_letter_random_two + numeral_random_two + spec_random_two
        return password

    def start(update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Пожалуйста, введите ваш логин:")
        return LOGIN

    def login(update: Update, context: CallbackContext) -> int:
        login = update.message.text
        password = generate_password()
        
        text = f"Здравствуйте, {login}.\n\nЛогин: {login.lower()}\nПароль: {password}"
        update.message.reply_text(text)
        return ConversationHandler.END

    def cancel(update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Операция отменена.")
        return ConversationHandler.END

    def main():
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
    