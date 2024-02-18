import sqlite3
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import requests

# SQLite database initialization
conn = sqlite3.connect('user_database.db',  check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        payment_complete INTEGER DEFAULT 0
    )
''')
conn.commit()

class BotFlow:
    @staticmethod
    def start(update, context):
        user = update.effective_user
        
        cursor.execute("INSERT INTO users (user_id, username, payment_complete) VALUES (?, ?, ?)", 
                   (user.id, user.username, False))
        conn.commit()
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome, {user.first_name}! How can I assist you today?")
        keyboard = [[InlineKeyboardButton("Complete Payment", callback_data='complete_payment')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please complete the payment to access more features.", reply_markup=reply_markup)

    @staticmethod
    def button_click(update, context):
        query = update.callback_query
        if query.data == 'complete_payment':
            user_id = query.from_user.id
            cursor.execute("UPDATE users SET is_payment_completed = 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            context.bot.answer_callback_query(callback_query_id=query.id, text="Payment completed successfully! You can now access more features.")
            BotFlow.send_message(update, context)

    @staticmethod
    def send_message(update, context):
        user_id = update.effective_user.id
        cursor.execute("SELECT is_payment_completed FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result and result[0] == 1:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please type your message:")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You need to complete payment first.")

    @staticmethod
    def receive_message(update, context):
        user_message = update.message.text
        response = requests.post('https://example.com/publish', json={'message': user_message})
        if response.status_code == 200:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Message sent successfully!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to send message. Please try again later.")


def main():
    # Telegram bot initialization
    updater = Updater(token='816748560:xM5H9nWPSdR8COe5DDFRFdZAaoXKNS98mGwL5cvG',
                       base_url="https://tapi.bale.ai/")
    dispatcher = updater.dispatcher
    dispatcher.bot.delete_webhook()
    
    # Handlers
    start_handler = MessageHandler(Filters.text("/start"), BotFlow.start)
    button_handler = CallbackQueryHandler(BotFlow.button_click)
    message_handler = MessageHandler(Filters.text & ~Filters.command, BotFlow.receive_message)

    # Adding handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(message_handler)

    # Start polling
    updater.start_polling()
    # updater.idle()

if __name__ == '__main__':
    main()
