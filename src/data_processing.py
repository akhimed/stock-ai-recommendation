import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds financial indicators to stock data:
    - Daily returns
    - 7-day & 30-day moving averages
    - Rolling volatility
    """
    df = df.copy()
    
    # Ensure data is sorted by date
    df = df.sort_values("date").reset_index(drop=True)

    # Daily return
    df["daily_return"] = df["close"].pct_change()

    # Moving averages
    df["sma_7"] = df["close"].rolling(window=7).mean()
    df["sma_30"] = df["close"].rolling(window=30).mean()

    # Rolling volatility (std dev of returns)
    df["volatility"] = df["daily_return"].rolling(window=7).std()

    return df

if __name__ == "__main__":
    from data_ingestion import get_historical_data
    
    # Example usage
    df = get_historical_data("AAPL", 60)
    processed_df = add_features(df)
    print(processed_df.tail(10))
