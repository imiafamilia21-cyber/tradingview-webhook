from flask import Flask, request, jsonify
import requests
import traceback

TELEGRAM_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

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
    print("📣 Вызов send_telegram()")
    print("📦 Telegram payload:", payload)
    print("📦 Telegram headers:", headers)
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print("📤 Telegram статус:", response.status_code)
        print("📤 Telegram ответ:", response.text)
    except Exception as e:
        print("❌ Ошибка Telegram:", e)
        traceback.print_exc()

app = Flask(__name__)

@app.route('/copilot', methods=['POST'])
def copilot_signal():
    try:
        data = request.get_json(force=True)
        print("📥 Получен JSON:", data)
        message = data.get("message", "📢 Сигнал от Копи!")
        print("🤖 Сигнал от Copilot:", message)
        send_telegram(message)
        return jsonify({"status": "sent", "message": message}), 200
    except Exception as e:
        print("❌ Ошибка в copilot_signal:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test_telegram():
    test_message = "🧪 Тестовое сообщение от /test"
    print("🚦 Тестовая отправка:", test_message)
    send_telegram(test_message)
    return "✅ Тестовое сообщение отправлено", 200

@app.route('/', methods=['GET'])
def home():
    return "🚀 XRPBot Webhook is running at /copilot"

if __name__ == "__main__":
    app.run(debug=True)
