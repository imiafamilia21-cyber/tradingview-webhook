from flask import Flask, request, jsonify
import requests
import traceback

# ?? Telegram настройки
TELEGRAM_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

# ?? Отправка сообщения в Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print("?? Telegram статус:", response.status_code)
        print("?? Telegram ответ:", response.text)
        if response.status_code == 200 and response.json().get("ok"):
            return True
        return False
    except Exception as e:
        print("? Ошибка Telegram:", e)
        traceback.print_exc()
        return False

# ?? Flask-приложение
app = Flask(__name__)

# ?? Основной маршрут для Copilot
@app.route('/copilot', methods=['POST', 'GET'])
def copilot_signal():
    try:
        if request.method == 'POST':
            data = request.get_json(force=True) if request.is_json else request.form
            message = data.get("message", "?? Сигнал от Копи!")
        else:
            message = "?? GET запрос к /copilot"

        print("?? Сигнал от Copilot:", message)
        success = send_telegram(message)
        if success:
            return jsonify({"status": "sent", "message": message}), 200
        else:
            return jsonify({"error": "Не удалось отправить в Telegram"}), 500
    except Exception as e:
        print("? Ошибка в copilot_signal:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ?? Тестовый маршрут
@app.route('/test', methods=['GET'])
@app.route('/test/<message>', methods=['GET'])
def test_telegram(message=None):
    test_message = message or "?? Тестовое сообщение от /test маршрута"
    print("?? Тестовая отправка:", test_message)
    success = send_telegram(test_message)
    if success:
        return f"? Тестовое сообщение отправлено: {test_message}", 200
    else:
        return "? Ошибка отправки тестового сообщения", 500

# ?? Домашняя страница
@app.route('/', methods=['GET'])
def home():
    return "?? XRPBot Webhook is running at /copilot"

if __name__ == "__main__":
    print("?? Запуск Flask приложения...")
    print(f"?? Токен: {TELEGRAM_TOKEN[:10]}...")
    print(f"?? Chat ID: {TELEGRAM_CHAT_ID}")
    app.run(debug=True, host="0.0.0.0", port=5000)
