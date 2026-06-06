import os
import time
import requests
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = '7798641801:AAHZWpVGv2YicowZaigNS9Q7jIHu9S3Jxaw'
CHAT_ID = '7803661441'

print("✅ Бот запускается...")

# Отправляем приветственное сообщение при старте
try:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': '✅ Бот запущен и работает!'}
    r = requests.post(url, data=data, timeout=5)
    print(f"✅ Тест отправлен, ответ: {r.status_code}")
except Exception as e:
    print(f"❌ Ошибка при тесте: {e}")

# Проверяем новые сообщения
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
                    if 'message' in upd:
                        chat = upd['message']['chat']['id']
                        text = upd['message'].get('text', '')
                        if text == '/start':
                            send_msg(chat, "✅ Бот активен! Используй /info")
                        elif text == '/info':
                            send_msg(chat, "📡 RAT сервер работает!")
                        else:
                            send_msg(chat, f"❌ Неизвестная команда: {text}")
        except Exception as e:
            print(f"Ошибка в listen: {e}")
        time.sleep(1)

def send_msg(chat, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': chat, 'text': text}
        requests.post(url, data=data, timeout=5)
    except:
        pass

import threading
threading.Thread(target=listen, daemon=True).start()

@app.route('/')
def home():
    return "✅ RAT сервер работает!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
