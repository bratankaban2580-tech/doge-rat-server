import os
import sys
from flask import Flask

app = Flask(__name__)

# ПРОВЕРКА: что видит сервер
token_from_env = os.environ.get('7798641801:AAHZWpVGv2YicowZaigNS9Q7jIHu9S3Jxaw')
print("=== ДИАГНОСТИКА ===")
print("Все переменные окружения:", dict(os.environ))
print("Токен из TELEGRAM_BOT_TOKEN:", repr(token_from_env))
sys.stdout.flush()  # принудительно выводим в лог

if not token_from_env:
    error_msg = "❌ ОШИБКА: TELEGRAM_BOT_TOKEN не задан!"
    print(error_msg)
else:
    print(f"✅ TOKEN НАЙДЕН: {token_from_env[:10]}... (обрезано)")

@app.route('/')
def home():
    return "✅ RAT сервер работает!", 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
