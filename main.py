import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

users = {}
quiz = [
    {
        "question": "India ka capital kya hai?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "answer": "Delhi"
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    }
]

current_q = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    if user_id not in users:
        users[user_id] = {"coins": 100}
    
    bot.send_message(user_id, f"👋 Welcome!\n💰 Coins: {users[user_id]['coins']}")
    send_quiz(user_id)

def send_quiz(user_id):
    q = random.choice(quiz)
    current_q[user_id] = q

    markup = InlineKeyboardMarkup()
    for opt in q["options"]:
        markup.add(InlineKeyboardButton(opt, callback_data=opt))

    bot.send_message(user_id, q["question"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    user_id = call.message.chat.id

    # 🔥 FIX: check if question exists
    if user_id not in current_q:
        bot.answer_callback_query(call.id, "⚠️ Start first using /start")
        return

    selected = call.data
    correct = current_q[user_id]["answer"]

    if selected == correct:
        users[user_id]["coins"] += 10
        bot.answer_callback_query(call.id, "✅ Sahi!")
        bot.send_message(user_id, f"🎉 +10 coins\n💰 Total: {users[user_id]['coins']}")
    else:
        users[user_id]["coins"] -= 5
        bot.answer_callback_query(call.id, "❌ Galat!")
        bot.send_message(user_id, f"➖ -5 coins\n💰 Total: {users[user_id]['coins']}")

    send_quiz(user_id)

@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.chat.id
    coins = users.get(user_id, {}).get("coins", 0)
    bot.send_message(user_id, f"💰 Your Coins: {coins}")

@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    sorted_users = sorted(users.items(), key=lambda x: x[1]["coins"], reverse=True)
    
    text = "🏆 Leaderboard:\n"
    for i, (uid, data) in enumerate(sorted_users[:5], start=1):
        text += f"{i}. {uid} → {data['coins']} coins\n"
    
    bot.send_message(message.chat.id, text)

print("Quiz Bot Running...")
bot.infinity_polling()
