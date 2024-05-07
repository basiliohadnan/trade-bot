import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        btc_price = data['bitcoin']['usd']
        return btc_price
    except Exception as e:
        print("Error fetching BTC price:", e)
        return None

def main():
    btc_price = fetch_price()
    if btc_price is not None:
        print(f"Current Bitcoin price: ${btc_price}")
    else:
        print("Failed to fetch Bitcoin price.")

if __name__ == "__main__":
    main()
