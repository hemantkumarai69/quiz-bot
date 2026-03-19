import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Simple question
question = "India ka capital kya hai?"
options = ["Delhi", "Mumbai", "Kolkata", "Chennai"]
correct_answer = "Delhi"

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    
    for option in options:
        markup.add(InlineKeyboardButton(option, callback_data=option))
    
    bot.send_message(message.chat.id, question, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == correct_answer:
        bot.answer_callback_query(call.id, "✅ Sahi jawab!")
        bot.send_message(call.message.chat.id, "🎉 You won!")
    else:
        bot.answer_callback_query(call.id, "❌ Galat jawab")

print("Quiz Bot Running...")
bot.infinity_polling()
