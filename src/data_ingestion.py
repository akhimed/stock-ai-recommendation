import requests
import pandas as pd
from datetime import datetime, timedelta
from config import POLYGON_API_KEY, BASE_URL

def get_historical_data(ticker="AAPL", days=30):
    """
    Fetch historical daily data for a given stock ticker.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    
    url = f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/{start_date:%Y-%m-%d}/{end_date:%Y-%m-%d}?adjusted=true&sort=asc&limit=500&apiKey={POLYGON_API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if "results" not in data:
        raise Exception(f"Error fetching data: {data}")
    
    df = pd.DataFrame(data["results"])
    df["t"] = pd.to_datetime(df["t"], unit="ms")  # convert timestamp
    df.rename(columns={"t": "date", "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}, inplace=True)
    
    return df

if __name__ == "__main__":
    df = get_historical_data("AAPL", 30)
    print(df.head())
