def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": str(message)
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        print("📤 Telegram статус:", response.status_code)
        print("📤 Telegram ответ:", response.text)
    except requests.exceptions.RequestException as e:
        print("❌ Ошибка Telegram:", e)
