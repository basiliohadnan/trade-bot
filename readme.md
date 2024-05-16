# Trade Bot

Trade Bot is a Python script designed to provide real-time monitoring and trading signals for Bitcoin based on various technical indicators.

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

## Usage

1. Run the `main.py` script:

   ```bash
   python main.py
   ```

2. Choose the mode of operation:
   - Enter `1` for Price Monitoring Mode: Monitors price changes and sends notifications based on predefined buying and selling signals.
   - Enter `2` for Price Tracking Mode: Tracks a specific condition provided by the user and sends a notification if met.

3. Follow the prompts to input the required parameters such as buy price and sell threshold.

4. The script will continuously run and provide real-time updates and trading signals via Telegram messages.

## Features

- Real-time monitoring of Bitcoin price changes.
- Price tracking mode with customizable conditions.
- Utilizes technical indicators such as Moving Averages (MA), Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD) for signal generation.
- Provides consolidated messages with price updates, trading signals, and percentage change since the start of the day.
- Telegram integration for receiving notifications.

## Requirements

- Python 3.x
- pandas
- schedule
- python-telegram-bot

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.