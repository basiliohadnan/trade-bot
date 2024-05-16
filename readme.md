# Trade Bot

This is a Python-based trade bot for monitoring Bitcoin prices and notifying you via Telegram. The bot can operate in two modes: 
1. Price Monitoring Mode: It sends regular updates about the Bitcoin price, including the current price, start of day price, lowest price of the day, highest price of the day, and percentage change since the start of the day.
2. Price Tracking Mode: It notifies you when the Bitcoin price increases by a specified percentage from a given buy price.

## Features

- Fetches current Bitcoin prices from CoinGecko API.
- Monitors and logs price changes.
- Sends consolidated price updates via Telegram.
- Tracks specific conditions and sends alerts when conditions are met.

## Requirements

- Python 3.x
- `requests`
- `pandas`
- `schedule`

## Installation

1. Clone the repository:

```sh
git clone https://github.com/basiliohadnan/trade-bot.git
cd trade-bot
```

2. Install the required Python packages:

```sh
pip install -r requirements.txt
```

3. Create a `constants.py` file and add your Telegram bot token and chat ID:

```python
# constants.py

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
INTERVAL_MINUTES = 5  # Interval in minutes for checking the price
```

## Usage

Run the main script and follow the prompts to select the mode and enter necessary details:

```sh
python main.py
```

### Example Usage

- **Price Monitoring Mode**: Select `1` to receive regular updates about Bitcoin prices.
- **Price Tracking Mode**: Select `2`, enter the buy price, and the percentage increase threshold to receive a notification when the condition is met.

## Code Overview

### Main Script (`main.py`)

The main script initializes global variables, defines job functions for monitoring price changes and tracking specific conditions, and runs the selected job at regular intervals.

### Bitcoin Price Fetching (`bitcoin.py`)

Contains functions to fetch the current Bitcoin price, calculate percentage changes, and get start of day prices from the CoinGecko API.

### Telegram Notifications (`telegram.py`)

Contains functions to send Telegram messages and log information.

### Constants (`constants.py`)

Stores the Telegram bot token, chat ID, and interval minutes.

## Contributing

Feel free to fork this repository and contribute by submitting a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CoinGecko API](https://www.coingecko.com/en/api) for providing the Bitcoin price data.
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/) for making Telegram integration easy.

```

### Instructions

1. Replace `"YOUR_TELEGRAM_BOT_TOKEN"` and `"YOUR_TELEGRAM_CHAT_ID"` in the `constants.py` file with your actual Telegram bot token and chat ID.
2. Run the bot using `python main.py` and follow the prompts to select the mode and input any required values.

### Running the Bot

```sh
python main.py
```

Choose `1` for Price Monitoring Mode or `2` for Price Tracking Mode, and the bot will start sending you the relevant updates via Telegram.