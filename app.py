import os
import time
import threading
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = '7798641801:AAHZWpVGv2YicowZaigNS9Q7jIHu9S3Jxaw'
CHAT_ID = '7803661441'

print("✅ Бот запускается...")

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': CHAT_ID, 'text': text}
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print(f"Ошибка: {e}")

def listen():
    last_id = 0
    send_telegram("✅ RAT сервер запущен!")
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {'offset': last_id + 1, 'timeout': 5}
            r = requests.get(url, params=params, timeout=6).json()
            if r.get('ok'):
                for update in r['result']:
                    last_id = update['update_id']
                    if 'message' in update:
                        chat = update['message']['chat']['id']
                        text = update['message'].get('text', '')
                        if text == '/start':
                            send_telegram("✅ Бот активен! Используй /info")
                        elif text == '/info':
                            send_telegram("📡 RAT сервер работает!")
                        else:
                            send_telegram(f"❌ Неизвестная команда: {text}")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(1)

threading.Thread(target=listen, daemon=True).start()

@app.route('/')
def home():
    return "✅ RAT сервер работает!", 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
