# Bitcoin Price Tracker

Bitcoin Price Tracker is a Python application that allows users to monitor Bitcoin prices and receive notifications based on user-defined conditions.

## Features

- **Price Monitoring Mode**: Allows users to monitor Bitcoin prices at regular intervals.
- **Price Tracking Mode**: Enables users to set a condition to track, such as a percentage increase from a buy price, and receive a notification when the condition is met.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/basiliohadnan/trade-bot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd trade-bot
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application by executing the `main.py` script:

```bash
python main.py
```

You will be prompted to select a mode:
- **Price Monitoring Mode (Option 1)**: Monitors Bitcoin prices at regular intervals.
- **Price Tracking Mode (Option 2)**: Tracks a specific condition, such as a percentage increase from a buy price.

### Price Monitoring Mode

In this mode, the application will continuously monitor Bitcoin prices at regular intervals and log the following information:

- Current Bitcoin price
- Start of day Bitcoin price
- New lowest and highest prices of the day
- Percentage change since the start of the day

### Price Tracking Mode

In this mode, the user must provide the following information:

- The price at which they bought Bitcoin (`buy_price`)
- The sell threshold percentage (e.g., 2 for 2%) (`sell_threshold`)

The application will then track the percentage change from the buy price and send a notification when it exceeds the sell threshold.

## Configuration

Before running the application, ensure that the `constants.py` file contains the correct configuration parameters, such as the interval for price monitoring.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.