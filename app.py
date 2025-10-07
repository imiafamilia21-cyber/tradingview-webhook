from flask import Flask, request, jsonify
import requests

# 🔐 Telegram настройки
TELEGRAM_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

# 📲 Отправка сообщения в Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": str(message)
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        print("📤 Telegram статус:", response.status_code)
        print("📤 Telegram ответ:", response.text)
    except requests.exceptions.RequestException as e:
        print("❌ Ошибка Telegram:", e)

# 🚀 Flask-приложение
app = Flask(__name__)

# 🔔 Маршрут для Copilot
@app.route('/copilot', methods=['POST'])
def copilot_signal():
    data = request.get_json(force=True)
    message = data.get("message", "📢 Сигнал от Копи!")
    print("🤖 Сигнал от Copilot:", message)
    send_telegram(message)
    return jsonify({"status": "sent", "message": message}), 200

# 🧪 Тестовый маршрут
@app.route('/test', methods=['GET'])
def test_telegram():
    test_message = "🧪 Тестовое сообщение от /test"
    print("🚦 Тестовая отправка:", test_message)
    send_telegram(test_message)
    return "✅ Тестовое сообщение отправлено", 200

# 🌐 Домашняя страница
@app.route('/', methods=['GET'])
def home():
    return "🚀 XRPBot Webhook is running at /copilot"

if __name__ == "__main__":
    app.run(debug=True)
