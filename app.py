import streamlit as st
import pandas as pd
from src.fetch_news import get_stock_news
from src.sentiment_model import get_sentiment

# -----------------------------
st.set_page_config(page_title="📈 Stock Sentiment Analyzer", layout="wide")
st.title("📈 Stock Sentiment Analyzer (Multi-source)")

# -----------------------------
# Popular companies dropdown
companies = {
    "Reliance Industries": "RELIANCE",
    "Tata Consultancy Services": "TCS",
    "Infosys": "INFY",
    "HDFC Bank": "HDFCBANK",
    "ICICI Bank": "ICICIBANK"
}

selected_company = st.selectbox("Select Company", list(companies.keys()))
custom_input = st.text_input("Or enter any company/ticker manually:")

# Determine query and ticker
if custom_input.strip() != "":
    query = custom_input.strip()
    ticker = None
else:
    query = selected_company
    ticker = companies[selected_company]

# Optional: NewsData.io API key
api_key = st.text_input("Optional: Enter NewsData.io API key (free tier)")

# -----------------------------
if st.button("Analyze Sentiment"):
    with st.spinner("Fetching news from multiple sources..."):
        articles = get_stock_news(query=query, ticker=ticker, api_key=api_key, pages=3)

    if not articles:
        st.warning("No articles found for this stock.")
    else:
        results = []
        for art in articles:
            try:
                text = art.get("title", "")
                sentiment, score = get_sentiment(text)
                results.append({
                    "Title": art.get("title"),
                    "Sentiment": sentiment,
                    "Score": score,
                    "URL": art.get("url"),
                    "Source": art.get("source")
                })
            except Exception as e:
                continue

        df = pd.DataFrame(results)
        st.dataframe(df)

        # -----------------------------
        if not df.empty:
            # Overall sentiment
            avg_score = df["Score"].mean()
            overall_sentiment = df["Sentiment"].mode()[0]
            st.markdown(f"### 🧭 Overall Sentiment for **{query}**: **{overall_sentiment}** (Avg score: {avg_score:.2f})")

            # Plot sentiment counts
            sentiment_counts = df["Sentiment"].value_counts()
            st.bar_chart(sentiment_counts)

            # Optional: show URLs
            with st.expander("Show article links"):
                for _, row in df.iterrows():
                    st.markdown(f"- [{row['Title']}]({row['URL']}) - {row['Source']}")
