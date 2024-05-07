# Crypto Price Tracker

This Python script fetches the current price of Bitcoin (BTC) from the CoinGecko API and displays it on the console. It also calculates the percentage change in price compared to the first run, the previous run, and the start of the day.

## Features

- Fetches the current price of Bitcoin (BTC) from the CoinGecko API.
- Calculates and displays the percentage change in price compared to the first run, the previous run, and the start of the day.
- Logs the fetched prices along with the percentage changes.

## Prerequisites

- Python 3.6 or higher installed on your system.
- A CoinGecko API key. Sign up for a free account at [CoinGecko](https://www.coingecko.com/en/api) to get an API key.
- Install the required dependencies by running `pip install -r requirements.txt`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/basiliohadnan/trade-bot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd trade-bot
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your CoinGecko API key:

   ```
   COINGECKO_API_KEY=your_api_key_here
   ```

## Usage

1. Run the script using Python:

   ```bash
   python bitcoin_price.py
   ```

2. Enter the interval in minutes when prompted. This interval determines how often the script fetches the Bitcoin price and calculates the percentage changes.

3. The script will display the current Bitcoin price and the percentage changes since the first run, the previous run, and the start of the day.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues.

## License

This project is licensed under the [MIT License](LICENSE).