from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 Действующие параметры
BOT_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

# 📤 Отправка сообщения в Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"❌ Ошибка отправки: {response.text}")
        return False
    print("✅ Сообщение отправлено.")
    return True

# 📡 Приём сигнала через POST-запрос
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get('symbol')
    direction = data.get('direction')
    price = data.get('price')

    if not symbol or not direction or not price:
        return jsonify({"error": "Missing required fields"}), 400

    message = f"*Signal Received*\nSymbol: `{symbol}`\nDirection: *{direction}*\nPrice: `{price}`"
    success = send_telegram_message(message)

    return jsonify({"status": "ok" if success else "failed"})

# 🧪 Тест через браузер
@app.route('/test/<message>', methods=['GET'])
def test_message(message):
    print(f"🔔 Получен тестовый запрос: {message}")
    success = send_telegram_message(f"Тестовое сообщение: {message}")
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message
    })

# 🚀 Запуск локально
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
