import os
import requests
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

initial_price = None
previous_price = None
day_start_price = None

def fetch_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        current_price = data['bitcoin']['usd']
        return current_price
    except Exception as e:
        print(f"{datetime.utcnow()} - Error fetching BTC price: {e}")
        return None

def calculate_percentage_change(current_price, reference_price):
    if reference_price is None:
        return None
    else:
        percentage_change = ((current_price - reference_price) / reference_price) * 100
        return percentage_change

def get_day_start_price():
    # Calculate the start of the day in UTC time zone
    start_of_day_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_day_unix_timestamp = int(start_of_day_utc.timestamp())

    # Fetch historical prices for the day
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Find the nearest price data point before the start of the day
        day_start_price = None
        for point in data['prices']:
            timestamp = point[0] // 1000  # Convert milliseconds to seconds
            if timestamp < start_of_day_unix_timestamp:
                day_start_price = point[1]
            else:
                break
        
        return day_start_price
    except Exception as e:
        print(f"{datetime.utcnow()} - Error fetching start of day BTC price: {e}")
        return None

def job():
    global initial_price, previous_price, day_start_price
    current_price = fetch_price()
    
    if initial_price is None:
        initial_price = current_price
    
    if day_start_price is None:
        day_start_price = get_day_start_price()
    
    if current_price is not None:
        print(f"{datetime.utcnow()} - Current Bitcoin price: ${current_price}")
        
        percentage_change_since_first_run = calculate_percentage_change(current_price, initial_price)
        if percentage_change_since_first_run is not None:
            print(f"{datetime.utcnow()} - Percentage Change since first run: {percentage_change_since_first_run:.2f}%")
        
        percentage_change_since_day_start = calculate_percentage_change(current_price, day_start_price)
        if percentage_change_since_day_start is not None:
            print(f"{datetime.utcnow()} - Percentage Change since day start: {percentage_change_since_day_start:.2f}%")
    else:
        print(f"{datetime.utcnow()} - Failed to fetch Bitcoin price.")
    
    previous_price = current_price

def main(interval_minutes):
    global day_start_price
    # Log the start day price when main is called
    day_start_price = get_day_start_price()
    print(f"{datetime.utcnow()} - Start of day Bitcoin price: ${day_start_price}")
    
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
