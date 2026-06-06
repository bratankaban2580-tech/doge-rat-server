import os
import time
import requests
import traceback
from flask import Flask
from telegram import Bot
from telegram.ext import Updater, CommandHandler

app = Flask(__name__)

BOT_TOKEN = os.environ.get('7798641801:AAHZWpVGv2YicowZaigNS9Q7jIHu9S3Jxaw')
CHAT_ID = '7803661441'

print("🔍 Старт приложения...")
print("🔍 BOT_TOKEN =", BOT_TOKEN)

# Проверка: может ли бот отправить сообщение при старте
try:
    bot_check = Bot(BOT_TOKEN)
    bot_check.send_message(chat_id=CHAT_ID, text="🟢 Бот запускается на сервере...")
    print("✅ Тестовое сообщение отправлено!")
except Exception as e:
    print("❌ Ошибка при отправке тестового сообщения:")
    traceback.print_exc()

def start(update, context):
    update.message.reply_text('✅ Бот активен! Используй /info')

def info(update, context):
    update.message.reply_text('📡 RAT сервер работает!')

def run_bot():
    try:
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("info", info))
        updater.start_polling()
        print("✅ Бот запущен и слушает сообщения!")
        updater.idle()
    except Exception as e:
        print("❌ Ошибка в run_bot:")
        traceback.print_exc()

import threading
threading.Thread(target=run_bot, daemon=True).start()

@app.route('/')
def home():
    return "✅ RAT сервер работает!", 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
