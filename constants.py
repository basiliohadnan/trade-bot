import os

# Constants
BITCOIN_API_URL = "https://api.coingecko.com/api/v3"
BITCOIN_ID = "bitcoin"
VS_CURRENCY = "usd"
DAYS_HISTORY = 1

# Interval in minutes
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", 60))
