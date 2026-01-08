import telebot
from telebot import types
import os
import time

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')

bot = telebot.TeleBot(BOT_TOKEN)
print("🤖 Phantrics Bot Started!")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🎉 Phantrics Payment Bot!

📸 Send screenshot with:
Name
Amount
UTR")

@bot.message_handler(content_types=['photo'])
def payment(m):
    if not m.caption or len(m.caption.split('
')) < 3:
        bot.reply_to(m, "❌ Need 3 lines!")
        return
    
    lines = m.caption.split('
')
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅", callback_data="v"),
        types.InlineKeyboardButton("❌", callback_data="r")
    )
    
    bot.send_message(ADMIN_ID, f"💰 Payment

👤 {lines[0]}
💵 ₹{lines[1]}
🔢 {lines[2]}", reply_markup=markup)
    bot.reply_to(m, "✅ Submitted!")

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if c.data == "v":
        bot.answer_callback_query(c.id, "✅")
        bot.edit_message_text("✅ VERIFIED

" + c.message.text, c.message.chat.id, c.message.id)
    else:
        bot.answer_callback_query(c.id, "❌")
        bot.edit_message_text("❌ REJECTED

" + c.message.text, c.message.chat.id, c.message.id)

while True:
    try:
        bot.infinity_polling()
    except:
        time.sleep(5)
