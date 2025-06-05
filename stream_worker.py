import tweepy
from sentiment import clean_text, extract_tickers, detect_direction
from collections import defaultdict
from threading import Thread

with open("tickers.txt") as f:
    VALID_TICKERS = set(line.strip().upper() for line in f)

mentions = defaultdict(lambda: {'long': 0, 'short': 0, 'neutral': 0})

class StockStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        if tweet.text.startswith("RT"):
            return
        process_tweet(tweet.text)

def process_tweet(text):
    tickers = extract_tickers(clean_text(text), VALID_TICKERS)
    direction = detect_direction(text)
    for ticker in tickers:
        mentions[ticker][direction] += 1

def start_stream(bearer_token):
    stream = StockStream(bearer_token)
    try:
        stream.add_rules(tweepy.StreamRule("stock OR call OR put OR $AAPL OR $TSLA"))
    except Exception:
        pass
    stream.filter(tweet_fields=["text"])
