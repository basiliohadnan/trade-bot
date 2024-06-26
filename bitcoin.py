import requests
import pandas as pd
from datetime import datetime

def fetch_price():
    """Fetch the current Bitcoin price in usd."""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        response.raise_for_status()
        return response.json()['bitcoin']['usd']
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch current Bitcoin price: {e}")
        return None

def get_historical_data(days=1):
    """Fetch historical Bitcoin price data for the last 'days' days."""
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}')
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
        df.set_index('timestamp', inplace=True)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch historical Bitcoin data: {e}")
        return None

def calculate_indicators(df):
    """Calculate technical indicators."""
    df['MA50'] = df['price'].rolling(window=50).mean()
    df['MA200'] = df['price'].rolling(window=200).mean()
    df['RSI'] = compute_rsi(df['price'])
    return df

def compute_rsi(series, period=14):
    """Calculate the Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_day_start_price():
    """Fetch the start of the day Bitcoin price."""
    historical_data = get_historical_data(1)
    if historical_data is not None:
        start_of_day = historical_data.iloc[0]['price']
        return start_of_day
    return None

def get_lowest_price_of_day(historical_data):
    """Retrieve the lowest price of the day from historical data."""
    if historical_data is not None:
        lowest_price = historical_data['price'].min()
        return lowest_price
    return None

def get_highest_price_of_day(historical_data):
    """Retrieve the highest price of the day from historical data."""
    if historical_data is not None:
        highest_price = historical_data['price'].max()
        return highest_price
    return None

def calculate_percentage_change(current_price, reference_price):
    """Calculate the percentage change between two prices."""
    if reference_price == 0:
        return 0
    return ((current_price - reference_price) / reference_price) * 100
