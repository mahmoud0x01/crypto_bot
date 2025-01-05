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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the /start command is issued, if from allowed chat ID."""
    if str(update.message.chat_id) == str(chat_id):
        await update.message.reply_text("Hello! You're authorized to use this bot.")
        print("someone clicked start")
    else:
        await update.message.reply_text("You're not authorized to use this bot.")


def run_bot() -> None:
    """Start the bot and listen for commands."""
    # Create the Application and pass the bot's token
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))



run_bot()