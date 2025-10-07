from flask import Flask, request, jsonify
import requests
import traceback
import time

# 🔐 Telegram настройки
TELEGRAM_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

# 📲 Альтернативные методы отправки в Telegram
def send_telegram(message):
    print(f"🧠 Отправка сообщения: {message}")

    # Метод 1: Стандартный JSON
    def method_json():
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            print(f"📡 Метод JSON - Статус: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print("✅ Сообщение отправлено (JSON метод)")
                    return True
            print(f"❌ JSON метод ошибка: {response.text}")
            return False
        except Exception as e:
            print(f"❌ JSON метод исключение: {e}")
            return False

    # Метод 2: Form-data
    def method_form_data():
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, data=payload, timeout=10)
            print(f"📡 Метод Form-data - Статус: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print("✅ Сообщение отправлено (Form-data метод)")
                    return True
            print(f"❌ Form-data метод ошибка: {response.text}")
            return False
        except Exception as e:
            print(f"❌ Form-data метод исключение: {e}")
            return False

    # Метод 3: Без parse_mode
    def method_simple():
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            print(f"📡 Метод Simple - Статус: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print("✅ Сообщение отправлено (Simple метод)")
                    return True
            print(f"❌ Simple метод ошибка: {response.text}")
            return False
        except Exception as e:
            print(f"❌ Simple метод исключение: {e}")
            return False

    # Метод 4: Проверка бота
    def check_bot():
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
        try:
            response = requests.get(url, timeout=10)
            print(f"🤖 Проверка бота - Статус: {response.status_code}")
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    print(f"✅ Бот активен: {bot_info['result']['username']}")
                    return True
            print(f"❌ Ошибка проверки бота: {response.text}")
            return False
        except Exception as e:
            print(f"❌ Ошибка проверки бота: {e}")
            return False

    # Запускаем проверки
    print("🔍 Проверяем доступность бота...")
    if not check_bot():
        print("❌ Бот недоступен или токен неверный")
        return False

    # Пробуем разные методы отправки
    methods = [method_json, method_form_data, method_simple]

    for i, method in enumerate(methods, 1):
        print(f"\n🔄 Попытка {i}: {method.__name__}")
        if method():
            return True
        time.sleep(1)  # Небольшая пауза между попытками

    print("❌ Все методы отправки не сработали")
    return False

# 🚀 Flask-приложение
app = Flask(__name__)

# 🔔 Основной маршрут для Copilot
@app.route('/copilot', methods=['POST', 'GET'])
def copilot_signal():
    try:
        if request.method == 'POST':
            data = request.get_json(force=True) if request.is_json else request.form
            print("📥 Получены данные:", data)
            message = data.get("message", "📢 Сигнал от Копи!")
        else:
            message = "📢 GET запрос к /copilot"

        print("🤖 Обрабатываем сообщение:", message)

        success = send_telegram(message)

        if success:
            return jsonify({"status": "sent", "message": message}), 200
        else:
            return jsonify({"error": "Не удалось отправить в Telegram"}), 500

    except Exception as e:
        print("❌ Ошибка в copilot_signal:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# 🧪 Расширенный тестовый маршрут
@app.route('/test', methods=['GET'])
@app.route('/test/<message>', methods=['GET'])
def test_telegram(message=None):
    test_message = message or "🧪 Тестовое сообщение от /test маршрута"
    print("🚦 Тестовая отправка:", test_message)

    success = send_telegram(test_message)

    if success:
        return f"✅ Тестовое сообщение отправлено: {test_message}", 200
    else:
        return "❌ Ошибка отправки тестового сообщения", 500

# 🔧 Проверка конфигурации
@app.route('/debug', methods=['GET'])
def debug_info():
    info = {
        "token_exists": bool(TELEGRAM_TOKEN),
        "token_length": len(TELEGRAM_TOKEN),
        "chat_id": TELEGRAM_CHAT_ID,
        "endpoints": {
            "home": "/",
            "copilot": "/copilot",
            "test": "/test",
            "debug": "/debug"
        }
    }
    return jsonify(info)

# 🌐 Домашняя страница
@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head><title>XRPBot Webhook</title></head>
        <body>
            <h1>🚀 XRPBot Webhook is running</h1>
            <p>Доступные маршруты:</p>
            <ul>
                <li><strong>POST /copilot</strong> - для получения сигналов</li>
                <li><strong>GET /test</strong> - тест отправки</li>
                <li><strong>GET /test/ваше_сообщение</strong> - тест с кастомным сообщением</li>
                <li><strong>GET /debug</strong> - отладочная информация</li>
            </ul>
        </body>
    </html>
    """

if __name__ == "__main__":
    print("🚀 Запуск Flask приложения...")
    print(f"🔐 Токен: {TELEGRAM_TOKEN[:10]}...")
    print(f"💬 Chat ID: {TELEGRAM_CHAT_ID}")
    app.run(debug=True, host='0.0.0.0', port=5000)
