import schedule
import time
from bitcoin import fetch_price, calculate_indicators, get_historical_data, get_day_start_price, calculate_percentage_change
from telegram import send_telegram_message, log_info
from constants import INTERVAL_MINUTES
import pandas as pd

# Initialize variables
initial_price = None
day_start_price = None
lowest_price_of_day = None
highest_price_of_day = None

def monitor_price_changes():
    """Monitors price changes and sends notifications."""
    global initial_price, day_start_price, lowest_price_of_day, highest_price_of_day
    historical_data = get_historical_data(30)
    if historical_data is None:
        log_info("Failed to fetch historical Bitcoin data.")
        return

    historical_data = calculate_indicators(historical_data)
    current_price = fetch_price()
    if current_price is None:
        log_info("Failed to fetch current Bitcoin price.")
        return

    if initial_price is None:
        initial_price = current_price

    if day_start_price is None:
        day_start_price = get_day_start_price()

    if lowest_price_of_day is None or current_price < lowest_price_of_day:
        lowest_price_of_day = current_price

    if highest_price_of_day is None or current_price > highest_price_of_day:
        highest_price_of_day = current_price

    percentage_change_since_day_start = calculate_percentage_change(current_price, day_start_price)

    # Check for buying signals
    latest_data = historical_data.iloc[-1]
    buy_signal = False
    if latest_data['RSI'] < 30:
        send_telegram_message("RSI below 30: Consider buying Bitcoin.")
        buy_signal = True
    if latest_data['MA50'] > latest_data['MA200'] and current_price > latest_data['MA50']:
        send_telegram_message("Golden Cross: 50-day MA crossed above 200-day MA. Consider buying Bitcoin.")
        buy_signal = True

    # Check for selling signals
    sell_signal = False
    if latest_data['RSI'] > 70:
        send_telegram_message("RSI above 70: Consider selling Bitcoin.")
        sell_signal = True
    if latest_data['MA50'] < latest_data['MA200'] and current_price < latest_data['MA50']:
        send_telegram_message("Death Cross: 50-day MA crossed below 200-day MA. Consider selling Bitcoin.")
        sell_signal = True

    # Consolidated message
    message = (
        f"Bitcoin Price Update:\n"
        f"Current Price: R${current_price:.2f}\n"
        f"Start of Day Price: R${day_start_price:.2f}\n"
        f"Lowest Price of the Day: R${lowest_price_of_day:.2f}\n"
        f"Highest Price of the Day: R${highest_price_of_day:.2f}\n"
        f"Percentage Change since day start: {percentage_change_since_day_start:.2f}%\n"
    )

    if buy_signal and sell_signal:
        send_telegram_message("Conflicting signals for Bitcoin. Please analyze the situation manually.")
    elif buy_signal:
        message += "Suggestion: Buy Bitcoin."
    elif sell_signal:
        message += "Suggestion: Sell Bitcoin."

    send_telegram_message(message)

def track_condition(buy_price, sell_threshold):
    """Tracks a specific condition and sends notification if met."""
    current_price = fetch_price()
    if current_price is None:
        log_info("Failed to fetch current Bitcoin price.")
        return

    percentage_change_from_buy_price = calculate_percentage_change(current_price, buy_price)
    if percentage_change_from_buy_price >= sell_threshold:
        send_telegram_message("Time to sell Bitcoin! Price has increased by 2% from buy price.")

def main():
    """Main function to run the application."""
    # Ask user for mode selection
    mode = input("Enter '1' for Price Monitoring Mode or '2' for Price Tracking Mode: ")
    if mode == '1':
        # Run job once immediately and schedule it for regular intervals
        monitor_price_changes()
        schedule.every(INTERVAL_MINUTES).minutes.do(monitor_price_changes)
    elif mode == '2':
        buy_price = float(input("Enter the price at which you bought Bitcoin: "))
        sell_threshold = float(input("Enter the sell threshold percentage (e.g., 2 for 2%): "))
        
        # Run job once immediately and schedule it for regular intervals
        track_condition(buy_price, sell_threshold)
        schedule.every(INTERVAL_MINUTES).minutes.do(track_condition, buy_price, sell_threshold)

    # Keep the script running to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
