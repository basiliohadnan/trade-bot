import os
import requests
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

initial_price = None
previous_price = None

def fetch_price():
    global previous_price
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

def calculate_percentage_change(current_price):
    global initial_price
    if initial_price is None:
        return None
    else:
        percentage_change = ((current_price - initial_price) / initial_price) * 100
        return percentage_change

def job():
    global initial_price, previous_price
    current_price = fetch_price()
    if initial_price is None:
        initial_price = current_price
    if current_price is not None:
        print(f"{datetime.utcnow()} - Current Bitcoin price: ${current_price}")
        percentage_change = calculate_percentage_change(current_price)
        if percentage_change is not None:
            print(f"{datetime.utcnow()} - Percentage Change since first run: {percentage_change:.2f}%")
    else:
        print(f"{datetime.utcnow()} - Failed to fetch Bitcoin price.")
    previous_price = current_price

def main(interval_minutes):
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
