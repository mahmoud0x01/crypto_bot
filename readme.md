## Crypto Trader

`a crypto currency trader bot that supports multi instance automated and manual trading of assets and controllable interface using telegram bot commands!`

### 

## Features :

1. listening on signals of **buy / sell** automatically from **TradingView** Strategies / algorithms using **thirdparty free service**  `mailgun` 
2. executing orders of buy / sell on any required supported asset by remote exchange `we implemented bybit using their API`
3. Calculating Comprehensive **Statistics** about your trading **{Realized PL , Unrealized PL, Others..}** of ***profits/losses*** also setting up calculation of **trading fees** of each trade been made!
4. **Stop loss / Take profit** supported by the bot efficiently 
5. **Pause / resume** bot at any time you want also saving the parameters of it!
6. running as many crypto bot instances as you want!
7. **Simulate** crypto **strategy** by running a bot instance with parameter `Simulation` making you able to **test strategy** in real time **without risk !**
8. Trade your crypto manually by creating a bot instance with a nonexistent mail listener and  executing command `/trigger_signal` and benefit from all Statistics , SL,TP ,other features!
9. A secure bot! only you can use your created bot by setting up your **chat_id** with the bot. for all other users bot replies with Unauthorized message



## Setup :

 to be able to use my bot . you need to do the following

1. install required models by using **pip**

   `pip3 install -r requirements.txt`

2. create telegram bot at **botfather** of telegram and get the bot_token and chat_id of your account with the bot and set it at global variable : `bot_token,chat_id` 

3. Register at **mailgun** and generate **api key** and also bring **domain name** that was generated in your account 

4. setup global vars : `domain_name , API_KEY` accordingly 

5. create wild card prefix **filter** word for i**ncoming emails** at **mailgun** and keep the **filtered word for receiving emails** in your mind for example receiving emails only at `something@domain....`  You gonna need this filter word later . filter can be like `match_recipient("something(.*?)@sandbo..\.mailgun\.org")`

6. knowing filtered wild card word . go to **Tradingview** . just make your strategy generate **Alerts**  as any normal crypto strategy or indicator there! and setting target email address as alert destination to your `something_someword@sandox....mailgun.org` 

   `To receive the confirmation code for tradingview you can use same mailgun api to retrieve message data. same code we use in the script`

7. Now you have your **wildcard prefix + selected word** when creating a bot using our script . you will enter it at prompt `Please enter your bot email listener : ` 

8. **Bybit** or another exchange **api keys** **required** and setup at or accordingly like global vars  `BB_API_KEY ,BB_SECRET_KEY `

9. You are all to go! 

## Telegram Bot commands: 

start - `start bot`  this is just start of controller itself not crypto trading instances
balance - `Account Balance`
create_bot - `create new bot` 
halt_bot - `pause trading instance`
resume_bot - `resume trading`
stop_bot - `stop trading bot`
show_bot_status - `show status`
set_st - `stop loss`
set_tp - `take profit`
list_bots - `list active bots`
list_signals - `list received signals`
trigger_signal - `Manual Buy or Sell`