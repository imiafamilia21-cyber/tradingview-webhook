from flask import Flask, request, jsonify
import requests

# 🔐 Telegram настройки
TELEGRAM_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

# 📲 Надёжная отправка сообщения в Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print("📤 Telegram статус:", response.status_code)
        print("📤 Telegram ответ:", response.text)
    except Exception as e:
        print("❌ Ошибка Telegram:", e)

# 🚀 Flask-приложение
app = Flask(__name__)

# 🔔 Основной маршрут для Copilot
@app.route('/copilot', methods=['POST'])
