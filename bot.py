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

def command_filter(command): 

    match = re.search(r'\b(Sell|Buy)\b', command, re.IGNORECASE)

    if match:
        word = match.group()
        word = word[0].upper() + word[1:]
        return word  # Output: sell
    else:
        return 0



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


    def truncate_float(self,value, precision):
        if ( precision > 4):
            precision = precision - 2
        # Convert to string with enough precision
        str_value = f"{value:.{precision + 2}f}"  # Add extra space to avoid rounding
        # Find the decimal point
        if '.' in str_value:
            integer_part, decimal_part = str_value.split('.')
            # Truncate the decimal part
            truncated_decimal = decimal_part[:precision]
            # Combine back the integer and truncated decimal parts
            return f"{integer_part}.{truncated_decimal}" if truncated_decimal else integer_part
        return str_value


    def Send_Orders(self):
        while self.running:
            with self.pause_condition:
                while self.paused:
                    self.pause_condition.wait()
                #send_telegram_message(f"{self.name} we here")
                # Construct the URL for retrieving events
                try:
                    events_url = f"https://api.mailgun.net/v3/{domain_name}/events"
                    #send_telegram_message(f"{self.name}send orders is running") 
                    # Parameters for filtering and pagination (optional)
                    params = {
                        "event": "stored",  # Filter by event type
                        "ascending": "no",   # Sort direction (yes or no)
                        "recipients": f"{self.listener_email}@{domain_name}",   
                        "limit": 1
                            }

                    # Make the GET request to retrieve the events
                    response = requests.get(events_url, auth=("api", API_KEY), params=params)

                    # Check the response status
                    if response.status_code == 200:
                        # Parse the JSON response
                        data = response.json()

                        # Initialize a variable to store the last message body
                        last_message_body = None
                        for item in data.get("items", []):
                            timestamp = item.get('timestamp')
                            message = item.get('message', {})
                            storage = item.get('storage', {})  # Get the storage details

                            if storage:
                                storage_key = storage.get('key')  # Get the storage key
                                if storage_key:
                                    Body_plain_New = getmessagedata(storage_key)
                                    command = command_filter(Body_plain_New)
                                    if (command != self.last_command_received):
                                        if (self.skip_next_signal == 0):   # we do not want to trigger SELL twice and somehow this works because the email still receives buy order again which override last comamnd received! 
                                            ress = self.Execute_Orders(command)
                                            if(ress==1):
                                                return 1
                                            send_telegram_message("----------------------------------------")
                                        else:
                                            self.skip_next_signal = 0

                                    self.last_command_received = command
                except Exception as e:
                    send_telegram_message(f"Exception happened in Send_Orders{e}")

            time.sleep(10)

    def Execute_Orders(self,command):
        cl = self.cl

        # Determine order side and quantity
        if command == "Buy":
            side = command
            quantity = float(self.amount)
            #quantity = int(quantity * 100) / 100
            #print(f"Buying {quantity} {self.symbol}")
            send_telegram_message(f"_{self.name}_ *{self.mode} Mode* : Buying *{quantity}* {self.symbol}")
        elif command == "Sell":
            side = command
            if (self.Simulation_flag==0):  
                pair = self.symbol
                baseCoin =  pair[:pair.index('USDT')] # extract the basecoin str
                prec = cl.get_coin_info(coin=baseCoin)['result']['rows'][0]['chains'][0]['minAccuracy']
                quantity = self.get_assets(baseCoin) # get available asset to Trade
                quantity = self.truncate_float(quantity,int(prec)) 
                # quantity = int(quantity * 100) / 100
            else:
                quantity = float(self.amount)

            #print(f"Selling {quantity} {self.symbol}")
            send_telegram_message(f"_{self.name}_ *{self.mode} Mode* : Selling *{quantity}* {self.symbol}")
        else:
            #print(f"Invalid command: {command}")
            send_telegram_message(f"_{self.name}_ *{self.mode} Mode* : Invalid command: {command}")
            return 1

        try:
            if (self.Simulation_flag==0):
                r = cl.place_order(
                    category="spot",
                    symbol=f"{self.symbol}",
                    side=side,
                    orderType="Market",
                    qty=quantity,
                    marketUnit="baseCoin",
                )

                    # Log response
                #print(f"Order response: {r['retMsg']}\n")
                send_telegram_message(f"_{self.name}_ *{self.mode} Mode* : Order response: {r['retMsg']}\n")
            #timestamp_of_order = datetime.fromtimestamp(r['time']/1000.0)
            #timestamp_of_order += timedelta(hours=4)
            current_utc_time = datetime.utcnow()
            # Add 7 hours to get GMT+7
            gmt_plus_7_time = current_utc_time + timedelta(hours=7)
            # Format the time as needed, e.g., "YYYY-MM-DD HH:MM:SS"
            timestamp_of_order = gmt_plus_7_time.strftime("%Y-%m-%d %H:%M:%S")
            self.order_counter = self.order_counter + 1 
        except exceptions.InvalidRequestError as e:
            print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
            send_telegram_message(f"_{self.name}_ *{self.mode} Mode* ByBit API Request Error : {e.message}")
            return 1
        except exceptions.FailedRequestError as e:
            print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
            send_telegram_message(f"_{self.name}_ *{self.mode} Mode* HTTP Request Failed : {e.message}")
            return 1
        except Exception as e:
            print("Unexpected error:", e)
            send_telegram_message(f"_{self.name}_ *{self.mode} Mode* Unexpected error: {e}")
            return 1
 

    def manual_trigger(self,command):
        if (command == "Buy"):
            self.Execute_Orders("Buy")
             #self.last_command_received = "Sell"
            self.skip_next_signal = 1
            send_telegram_message(f" _{self.name}_ Executed manual_trigger)")
        elif(command == "Sell"):
            self.Execute_Orders("Sell")
             #self.last_command_received = "Sell"
            self.skip_next_signal = 1
            send_telegram_message(f" _{self.name}_ Executed manual_trigger)")

    def listlast_commands(self):
        listlast_commands = []
        events_url = f"https://api.mailgun.net/v3/{domain_name}/events"

        params = {
            "event": "stored",  # Filter by event type
            "ascending": "no",   # Sort direction (yes or no)
            "recipients": f"{self.listener_email}@{self.domain_name}",
            "limit": 20
        }


        response = requests.get(events_url, auth=("api", API_KEY), params=params)

        if response.status_code == 200:
            data = response.json()
            last_message_body = None
            for item in data.get("items", []):
                timestamp = item.get('timestamp')
                message = item.get('message', {})
                storage = item.get('storage', {})  # Get the storage details
                if storage:
                    storage_key = storage.get('key')  # Get the storage key
                    if storage_key:
                        Body_plain_New = getmessagedata(storage_key)
                        command = Body_plain_New
                        dt_object = datetime.fromtimestamp(timestamp)  # it just works fine without / 1000.0 
                        dt_object += timedelta(hours=4)
                        listlast_commands.append(f"{command}  {dt_object}")

        return listlast_commands

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