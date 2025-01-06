import requests








bot_token = "7871464466:AAGPsw9swPen6LqnmXebZbzCoVL4VjoCSGY"
chat_id = 836636054




def get_assets(coin):             # avbl = get_assets("SOL")
        cl = HTTP(
            api_key=BB_API_KEY,
            api_secret=BB_SECRET_KEY,
            recv_window=60000
        )
        r = cl.get_wallet_balance(accountType="UNIFIED")
        assets = {
            asset.get('coin') : float(asset.get('availableToWithdraw', '0.0'))
            for asset in r.get('result', {}).get('list', [])[0].get('coin', [])
        }
        return assets.get(coin, 0.0)



def get_account_balance():
    balance = get_assets("USDT")
    balance = round(balance,3)
    return balance



def get_usdt_to_rub(amount):
    try:
        # Get USDT to RUB conversion rate
        usdt_to_rub_url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
        rub_response = requests.get(usdt_to_rub_url)
        usd_to_rub_rate = float(rub_response.json()['conversion_rates']['RUB'])
        
        # Calculate total coin to RUB
        total_rub = amount * usd_to_rub_rate
        return total_rub
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching data: {e}")
        return None
        
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

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    if str(update.message.chat_id) == str(chat_id):
        balance = get_account_balance()
        balance_rub = get_usdt_to_rub(balance)
        send_telegram_message(f"```Account USD : {balance}\n RUB : {balance_rub} ```")            

    else:
        await query.edit_message_text(text="You're not authorized to use this bot.")


def run_bot() -> None:
    """Start the bot and listen for commands."""
    # Create the Application and pass the bot's token
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))



run_bot()