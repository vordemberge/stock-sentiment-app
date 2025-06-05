import streamlit as st
import matplotlib.pyplot as plt
import time
from stream_worker import mentions, start_stream, VALID_TICKERS
from threading import Thread

st.set_page_config(page_title="Twitter Stock Sentiment", layout="wide")
st.title("📈 Live Twitter Stock Sentiment Dashboard")

BEARER_TOKEN = st.secrets["BEARER_TOKEN"]

if 'streaming' not in st.session_state:
    t = Thread(target=start_stream, args=(BEARER_TOKEN,))
    t.daemon = True
    t.start()
    st.session_state.streaming = True

st.sidebar.header("Add a Ticker to Track")
new_ticker = st.sidebar.text_input("Enter a ticker (e.g. AAPL, TSLA):", max_chars=5)

if st.sidebar.button("Add Ticker"):
    if new_ticker:
        ticker_upper = new_ticker.strip().upper()
        if ticker_upper not in VALID_TICKERS:
            VALID_TICKERS.add(ticker_upper)
            st.sidebar.success(f"Added {ticker_upper} to tracking list!")
            with open("tickers.txt", "a") as f:
                f.write(ticker_upper + "\n")
        else:
            st.sidebar.warning(f"{ticker_upper} is already being tracked.")

st.subheader("Live Ticker Mentions")

while True:
    tickers = list(mentions.keys())
    long_counts = [mentions[t]['long'] for t in tickers]
    short_counts = [mentions[t]['short'] for t in tickers]

    fig, ax = plt.subplots()
    ax.bar(tickers, long_counts, label='Long', color='green')
    ax.bar(tickers, short_counts, bottom=long_counts, label='Short', color='red')
    ax.set_ylabel("Mentions")
    ax.set_xlabel("Tickers")
    ax.legend()
    st.pyplot(fig)
    time.sleep(10)
