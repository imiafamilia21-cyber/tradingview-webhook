from flask import Flask, request, jsonify
import requests

# 🔐 Telegram настройки
TELEGRAM_TOKEN = "8382189772:AAFlSgb8hr75EF1Ry6Q8_iFmK5ZvbSUqjFU"
TELEGRAM_CHAT_ID = "1913932382"

# 📲 Функция отправки сообщения в Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 200:
            print("Ошибка Telegram:", response.text)
    except Exception as e:
        print("Ошибка Telegram:", e)

# 🚀 Flask-приложение
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📡 Получен сигнал:", data)

    # 🧠 Формируем сообщение
    message = f"""
📡 Сигнал: {data.get('asset')} — {data.get('direction')}
🧠 Стратегия: {data.get('strategy')}
⚠️ Риск: {data.get('risk_percent')}%
📉 Просадка: -{data.get('drawdown_r')}R
🎯 TP: {data.get('TP_R')}R, SL: {data.get('SL_ATR')}×ATR
⏱️ Время: {data.get('timestamp')}
    """

    # 📲 Отправляем в Telegram
    send_telegram(message)

    # ✅ Возвращаем ответ TradingView
    return jsonify({"status": "received", "message": message}), 200
