import os
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


def job():
    """Performs the main job function."""
    current_price = fetch_price()
    if current_price is None:
        return

    log_info(f"Current Bitcoin price: ${current_price}")

    global initial_price, day_start_price, lowest_price_of_day, highest_price_of_day
    if initial_price is None:
        initial_price = current_price

    if day_start_price is None:
        lowest_price_of_day, highest_price_of_day = get_day_start_price()
        day_start_price = (lowest_price_of_day + highest_price_of_day) / 2  # Use average price as the day start price
        log_info(f"Start of day Bitcoin price: ${day_start_price}")

    if current_price < lowest_price_of_day:
        lowest_price_of_day = current_price
        log_info(f"New lowest price of the day: ${lowest_price_of_day}")

    if current_price > highest_price_of_day:
        highest_price_of_day = current_price
        log_info(f"New highest price of the day: ${highest_price_of_day}")

    if day_start_price is not None:
        percentage_change_since_day_start = calculate_percentage_change(current_price, day_start_price)
        log_info(f"Percentage Change since day start: {percentage_change_since_day_start:.2f}%")

    if lowest_price_of_day is not None:
        percentage_diff_from_lowest = calculate_percentage_change(current_price, lowest_price_of_day)
        log_info(f"Percentage Difference from Lowest Price of the Day: {percentage_diff_from_lowest:.2f}%")

    if highest_price_of_day is not None:
        percentage_diff_from_highest = calculate_percentage_change(current_price, highest_price_of_day)
        log_info(f"Percentage Difference from Highest Price of the Day: {percentage_diff_from_highest:.2f}%")


def main():
    """Main function to run the application."""
    # Run job once immediately
    job()

    # Schedule price fetching task at specified interval
    schedule.every(INTERVAL_MINUTES).minutes.do(job)

    # Keep the script running to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
