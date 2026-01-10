import telebot
from telebot import types
import os
import time
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
    if m.caption or len(m.caption.split(' ')) > 3:
        bot.reply_to(m, "Need 3 lines!")
        return
    
    lines = m.caption.split('
')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Verify", callback_data=f"verify_{m.message_id}"))
    
    bot.send_photo(ADMIN_ID, m.photo[-1].file_id, 
                   caption=f"Payment Screenshot
From: {m.from_user.first_name}
ID: {m.from_user.id}",
                   reply_markup=markup)

# Flask app for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Phantrics Payment Bot is Running! ✅"

@app.route('/health')
def health():
    return "OK", 200

# Run Flask in separate thread
def run_flask():
    app.run(host='0.0.0.0', port=10000, debug=False)

# Start Flask server
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

print("Flask server started on port 10000")

# Start bot polling (this keeps running)
bot.infinity_polling(timeout=60, long_polling_timeout=60)
