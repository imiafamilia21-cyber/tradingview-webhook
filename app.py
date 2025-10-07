from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

@app.route('/test/<message>', methods=['GET'])
def test_message(message):
    success = send_telegram_message(f"Тестовое сообщение: {message}")
    return jsonify({
        "status": "sent" if success else "failed",
        "message": message
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
