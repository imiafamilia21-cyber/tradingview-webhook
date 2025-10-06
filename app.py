from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📡 Получен сигнал:", data)

    message = f"""
📡 Сигнал: {data.get('asset')} — {data.get('direction')}
🧠 Стратегия: {data.get('strategy')}
⚠️ Риск: {data.get('risk_percent')}%
📉 Просадка: -{data.get('drawdown_r')}R
🎯 TP: {data.get('TP_R')}R, SL: {data.get('SL_ATR')}×ATR
⏱️ Время: {data.get('timestamp')}
    """

    return jsonify({"status": "received", "message": message}), 200
