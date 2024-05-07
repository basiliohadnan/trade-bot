import os
import requests
import schedule
import time
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Constants
BITCOIN_API_URL = "https://api.coingecko.com/api/v3"
BITCOIN_ID = "bitcoin"
VS_CURRENCY = "usd"
DAYS_HISTORY = 1

initial_price = None
day_start_price = None
lowest_price_of_day = None
highest_price_of_day = None

def fetch_price():
    """Fetches the current Bitcoin price."""
    try:
        url = f"{BITCOIN_API_URL}/simple/price?ids={BITCOIN_ID}&vs_currencies={VS_CURRENCY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[BITCOIN_ID][VS_CURRENCY]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Bitcoin price: {e}")
        return None

def calculate_percentage_change(current_price, reference_price):
    """Calculates the percentage change between two prices."""
    if reference_price is None:
        return None
    return ((current_price - reference_price) / reference_price) * 100

def get_day_start_price():
    """Fetches the start of day Bitcoin price."""
    try:
        start_of_day_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_day_unix_timestamp = int(start_of_day_utc.timestamp())
        url = f"{BITCOIN_API_URL}/coins/{BITCOIN_ID}/market_chart?vs_currency={VS_CURRENCY}&days={DAYS_HISTORY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Initialize lowest and highest prices with the first price point
        lowest_price = data['prices'][0][1]
        highest_price = data['prices'][0][1]

        # Iterate over the price points to find the lowest and highest prices
        for point in data['prices']:
            price = point[1]
            if price < lowest_price:
                lowest_price = price
            if price > highest_price:
                highest_price = price
        
        return lowest_price, highest_price

    except requests.RequestException as e:
        logging.error(f"Failed to fetch start of day BTC price: {e}")
        return None, None

def job():
    """Performs the main job function."""
    current_price = fetch_price()
    if current_price is None:
        return

    logging.info(f"Current Bitcoin price: ${current_price}")

    global initial_price, day_start_price, lowest_price_of_day, highest_price_of_day
    if initial_price is None:
        initial_price = current_price

    if day_start_price is None:
        lowest_price_of_day, highest_price_of_day = get_day_start_price()
        day_start_price = (lowest_price_of_day + highest_price_of_day) / 2  # Use average price as the day start price
        logging.info(f"Start of day Bitcoin price: ${day_start_price}")
    
    if current_price < lowest_price_of_day:
        lowest_price_of_day = current_price
        logging.info(f"New lowest price of the day: ${lowest_price_of_day}")
    
    if current_price > highest_price_of_day:
        highest_price_of_day = current_price
        logging.info(f"New highest price of the day: ${highest_price_of_day}")

    if day_start_price is not None:
        percentage_change_since_day_start = calculate_percentage_change(current_price, day_start_price)
        logging.info(f"Percentage Change since day start: {percentage_change_since_day_start:.2f}%")

    if lowest_price_of_day is not None:
        percentage_diff_from_lowest = calculate_percentage_change(current_price, lowest_price_of_day)
        logging.info(f"Percentage Difference from Lowest Price of the Day: {percentage_diff_from_lowest:.2f}%")

    if highest_price_of_day is not None:
        percentage_diff_from_highest = calculate_percentage_change(current_price, highest_price_of_day)
        logging.info(f"Percentage Difference from Highest Price of the Day: {percentage_diff_from_highest:.2f}%")

def main(interval_minutes):
    """Main function to run the application."""
    global initial_price, day_start_price, lowest_price_of_day, highest_price_of_day

    # Run job once immediately
    job()

    # Schedule price fetching task at specified interval
    schedule.every(interval_minutes).minutes.do(job)

    # Keep the script running to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    interval_minutes = int(input("Enter the interval in minutes: "))
    main(interval_minutes)
