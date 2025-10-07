from flask import Flask, request
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
    if response.status_code != 200:
        print(f"Ошибка отправки: {response.text}")
    else:
        print("Сообщение успешно отправлено.")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get('symbol')
    direction = data.get('direction')
    price = data.get('price')

    message = f"*Signal Received*\nSymbol: `{symbol}`\nDirection: *{direction}*\nPrice: `{price}`"
    send_telegram_message(message)

    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)
