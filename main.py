import schedule
import time
from bitcoin import fetch_price, calculate_percentage_change, get_day_start_price
from telegram import send_telegram_message, log_info
from constants import INTERVAL_MINUTES

# Initialize variables
initial_price = None
day_start_price = None
lowest_price_of_day = None
highest_price_of_day = None

def monitor_price_changes():
    """Monitors price changes and sends consolidated notifications."""
    current_price = fetch_price()
    if current_price is None:
        log_info("Failed to fetch current Bitcoin price.")
        return

    global initial_price, day_start_price, lowest_price_of_day, highest_price_of_day
    if initial_price is None:
        initial_price = current_price

    if day_start_price is None:
        price_data = get_day_start_price()
        if price_data is not None:
            lowest_price_of_day, highest_price_of_day = price_data
            day_start_price = (lowest_price_of_day + highest_price_of_day) / 2
        else:
            log_info("Failed to fetch start of day BTC price.")
            return

    if current_price < lowest_price_of_day:
        lowest_price_of_day = current_price

    if current_price > highest_price_of_day:
        highest_price_of_day = current_price

    if day_start_price is not None:
        percentage_change_since_day_start = calculate_percentage_change(current_price, day_start_price)

    # Prepare the consolidated message
    message = f"Bitcoin Price Update:\nCurrent Price: R$ {current_price:.2f}\nStart of Day Price: R$ {day_start_price:.2f}\nLowest Price of the Day: R$ {lowest_price_of_day:.2f}\nHighest Price of the Day: R$ {highest_price_of_day:.2f}\nPercentage Change since day start: {percentage_change_since_day_start:.2f}%"
    
    # Send the message
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
