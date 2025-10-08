from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
CHAT_ID = "1913932382"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=payload)
    print("Telegram response:", response.text)
    return response.status_code == 200

@app.route('/test/<message>', methods=['GET'])
def test(message):
    success = send_telegram_message(f"Тестовое сообщение: {message}")
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message
    })

# ✅ Новый маршрут — проверка Копи через браузер
@app.route('/copilot/<message>', methods=['GET'])
def copilot_browser(message):
    success = send_telegram_message(f"Сообщение от Копи: {message}")
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message
    })
