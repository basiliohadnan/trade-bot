import requests
import pandas as pd

def fetch_price():
    """Fetches the current price of Bitcoin in BRL."""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl')
        data = response.json()
        return data['bitcoin']['brl']
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def calculate_percentage_change(current_price, reference_price):
    """Calculates the percentage change between current price and reference price."""
    try:
        return ((current_price - reference_price) / reference_price) * 100
    except ZeroDivisionError:
        return float('inf')

def get_day_start_price():
    """Fetches the starting price of Bitcoin for the day."""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=brl&days=1')
        data = response.json()
        prices = data['prices']
        prices_df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
        start_of_day_price = prices_df['price'].iloc[0]
        lowest_price_of_day = prices_df['price'].min()
        highest_price_of_day = prices_df['price'].max()
        return lowest_price_of_day, highest_price_of_day
    except Exception as e:
        print(f"Error fetching day start price: {e}")
        return None

def get_historical_data():
    """Fetches historical price data for Bitcoin."""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=brl&days=30')
        data = response.json()
        prices = data['prices']
        prices_df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
        return prices_df
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None

def calculate_indicators(df):
    """Calculates technical indicators for given price data."""
    df['MA20'] = df['price'].rolling(window=20).mean()
    df['MA50'] = df['price'].rolling(window=50).mean()
    df['EMA20'] = df['price'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['price'].ewm(span=50, adjust=False).mean()
    return df
