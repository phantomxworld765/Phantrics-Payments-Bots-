import telebot
from telebot import types
import os
from flask import Flask
import threading

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))

bot = telebot.TeleBot(BOT_TOKEN)
print("Bot Started!")

# Start command
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Phantrics Payment Bot Active!")

# Payment handler
@bot.message_handler(content_types=['photo'])
def payment(m):
    if not m.caption:
        bot.reply_to(m, "Please add payment details!")
        return
    
    user_name = m.from_user.first_name
    user_id = m.from_user.id
    details = m.caption
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Approve", callback_data="approve"))
    
    msg = "Payment Received

From: " + str(m.from_user.first_name) + "
User ID: " + str(m.from_user.id) + "

Details:
" + m.caption
    
    bot.send_photo(ADMIN_ID, m.photo[-1].file_id, caption=msg, reply_markup=markup)
    bot.reply_to(m, "Payment submitted!")

# Flask app for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

@app.route('/health')
def health():
    return "OK"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

print("Flask started")

bot.infinity_polling(timeout=60, long_polling_timeout=60)
