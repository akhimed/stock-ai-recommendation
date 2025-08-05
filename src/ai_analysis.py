import openai
from config import OPENAI_API_KEY
import pandas as pd

# Set API key
openai.api_key = OPENAI_API_KEY

def summarize_metrics(df: pd.DataFrame) -> str:
    latest = df.iloc[-1]
    trend = "up" if latest["sma_7"] > latest["sma_30"] else "down"
    volatility = latest["volatility"]

    summary = (
        f"30-day trend: {trend}\n"
        f"Current price: {latest['close']:.2f}\n"
        f"7-day SMA: {latest['sma_7']:.2f}\n"
        f"30-day SMA: {latest['sma_30']:.2f}\n"
        f"Volatility (7-day): {volatility:.4f}"
    )
    return summary

def ai_recommendation(summary: str) -> str:
    prompt = f"""
You are a financial analyst. Based on the following stock summary, give a simple BUY, SELL, or HOLD recommendation with 1-2 sentences of reasoning:

{summary}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert stock analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    from data_ingestion import get_historical_data
    from data_processing import add_features

    # Fetch and process data
    df = get_historical_data("AAPL", 60)
    df = add_features(df)

    summary = summarize_metrics(df)
    print("Summary:\n", summary)

    recommendation = ai_recommendation(summary)
    print("\nAI Recommendation:\n", recommendation)
