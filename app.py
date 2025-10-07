from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 Укажи свои реальные значения
TOKEN = "твой_токен_бота"
CHAT_ID = "твой_chat_id"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    print("Telegram response:", response.text)  # 🔍 Для отладки
    return response.status_code == 200

# ✅ Маршрут для ручной проверки через браузер
@app.route('/test/<message>', methods=['GET'])
def test_message(message):
    success = send_telegram_message(f"Тестовое сообщение: {message}")
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message
    })

# ✅ Маршрут для автоматической отправки по POST
@app.route('/copilot', methods=['POST'])
def copilot_message():
    data = request.get_json()
    message = data.get("message", "Нет сообщения")
    success = send_telegram_message(f"Сообщение от Копи: {message}")
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message
    })
