import requests
from constants import BITCOIN_API_URL, BITCOIN_ID, VS_CURRENCY, DAYS_HISTORY


def fetch_price():
    """Fetches the current Bitcoin price."""
    try:
        url = f"{BITCOIN_API_URL}/simple/price?ids={BITCOIN_ID}&vs_currencies={VS_CURRENCY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[BITCOIN_ID][VS_CURRENCY]
    except requests.RequestException as e:
        print(f"Failed to fetch Bitcoin price: {e}")
        return None


def calculate_percentage_change(current_price, reference_price):
    """Calculates the percentage change between two prices."""
    if reference_price is None:
        return None
    return ((current_price - reference_price) / reference_price) * 100


def get_day_start_price():
    """Fetches the start of day Bitcoin price."""
    try:
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
        print(f"Failed to fetch start of day BTC price: {e}")
        return None, None
