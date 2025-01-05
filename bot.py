import requests








bot_token = "7871464466:AAGPsw9swPen6LqnmXebZbzCoVL4VjoCSGY"
chat_id = 836636054



def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  # Optional, use "Markdown" or "HTML" for formatting
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("telegram Message sent successfully")
    else:
        print("Failed to send message:", response.text)