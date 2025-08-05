import streamlit as st
import pandas as pd
from data_ingestion import get_historical_data
from data_processing import add_features
from ai_analysis import summarize_metrics, ai_recommendation
import plotly.graph_objects as go

# ---- STREAMLIT DASHBOARD ----
st.set_page_config(page_title="Stock AI Recommendation", layout="wide")

# Title
st.title("📈 Stock AI Recommendation Dashboard")

# Sidebar inputs
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
days = st.sidebar.slider("Number of days", min_value=30, max_value=180, value=60, step=10)

# Fetch and process data
try:
    with st.spinner("Fetching stock data..."):
        raw_df = get_historical_data(ticker, days)
        df = add_features(raw_df)

    # Summarize metrics for AI
    summary = summarize_metrics(df)
    recommendation = ai_recommendation(summary)

    # Display summary + AI recommendation
    st.subheader(f"AI Recommendation for {ticker}")
    st.markdown(f"**Summary:**\n```\n{summary}\n```")
    st.markdown(f"**Recommendation:** {recommendation}")

    # Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['sma_7'], mode='lines', name='7-day SMA'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['sma_30'], mode='lines', name='30-day SMA'))
    fig.update_layout(title=f"{ticker} Price & Moving Averages",
                      xaxis_title="Date", yaxis_title="Price",
                      hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Show data table
    st.subheader("Data Table")
    st.dataframe(df.tail(30))

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, f"{ticker}_data.csv", "text/csv")

except Exception as e:
    st.error(f"Error: {e}")
