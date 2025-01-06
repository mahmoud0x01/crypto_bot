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




class Traderbot(threading.Thread):
    _active_threads = []  # Class-level list to store all active threads
    #_id_counter = 1  # Class-level counter for unique thread IDs
    def __init__(self,id_t="Undefined",symbol="BTCUSDT",tp=0.0,sl=0.0,amount=0.00011,mode="Simulation",listener_email="any"):
        super().__init__()
        self.stop_thread = False
        self.paused = False  # Flag to control pausing
        self.pause_condition = threading.Condition()  # Condition to manage pausing
        self.name = id_t
        self.symbol = symbol #BTCUSDT , ETHUSDT
        self.amount = amount
        self.mode = (str(mode)).replace(" ", "") # Real , Simulation
        self.running = True  # Flag to control the loop in func1 and func2
        self.last_command_received = "Sell"
        self.last_price = 1.0
        self.accumulated_percentage_change = 0.0
        self.last_buy_price = 0.0
        self.listener_email = listener_email
        self.skip_next_signal = 0
        self.domain_name = domain_name
        self.order_counter = 0
        self.wins = 0
        self.loses = 0 
        if (self.mode == "Real"):
            self.Simulation_flag = 0
        elif (self.mode == "Simulation"):
            self.Simulation_flag = 1
        self.cl = HTTP(
            api_key=BB_API_KEY,
            api_secret=BB_SECRET_KEY,
            recv_window=60000
        )

        Traderbot._active_threads.append(self)  # Add this thread to the active threads list



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