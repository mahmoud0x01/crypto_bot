## Crypto Trader

`a crypto currency trader bot that supports multi instance automated and manual trading of assets and controllable interface using telegram bot commands!`

### 

### Features

- Listens to buy/sell signals from TradingView strategies via Mailgun.
- Executes buy/sell orders on supported assets using Bybit API.
- Provides detailed trading statistics (e.g., realized/unrealized P/L, fees).
- Supports stop-loss and take-profit functionality.
- Allows pausing and resuming bot instances.
- Enables multiple bot instances for different trading pairs.
- Includes a simulation mode to test strategies risk-free.
- Offers manual trading via Telegram bot commands.
- Ensures secure access through chat ID restrictions.



### Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Set up a Telegram bot via BotFather and configure the `bot_token` and `chat_id` variables.

3. Register with Mailgun and configure `API_KEY` and `domain_name`.

4. Create a wildcard prefix for TradingView alerts in Mailgun and set the alert email address.

5. Retrieve TradingView confirmation codes using the Mailgun API.

6. Configure Bybit API keys (`BB_API_KEY` and `BB_SECRET_KEY`).

### Telegram Bot Commands

- **/start**: Initializes the bot controller.
- **/balance**: Retrieves account balance.
- **/create_bot**: Sets up a new trading bot instance.
- **/halt_bot**: Pauses a bot instance.
- **/resume_bot**: Resumes a paused bot instance.
- **/stop_bot**: Stops and deletes a bot instance.
- **/show_bot_status**: Displays the status of a specific bot.
- **/set_st**: Configures stop-loss for a bot instance.
- **/set_tp**: Configures take-profit for a bot instance.
- **/list_bots**: Lists all active bot instances.
- **/list_signals**: Shows recent trading signals received.
- **/trigger_signal**: Manually triggers a buy or sell command.

------

### Useful Links

- [Telegram BotFather](https://core.telegram.org/bots#botfather)
- [Mailgun API Documentation](https://documentation.mailgun.com/en/latest/api_reference.html)
- [Bybit API Documentation](https://bybit-exchange.github.io/docs/)
- [Python PIP Documentation](https://pip.pypa.io/en/stable/)

