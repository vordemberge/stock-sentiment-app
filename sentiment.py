import re

LONG_KEYWORDS = ['buy', 'long', 'call', 'bullish', 'moon']
SHORT_KEYWORDS = ['sell', 'short', 'put', 'bearish', 'down']

def clean_text(text):
    return re.sub(r'http\S+|[^A-Z$ ]', '', text.upper())

def extract_tickers(text, valid_tickers):
    matches = re.findall(r'\$?[A-Z]{1,5}', text)
    return [m.replace('$', '') for m in matches if m.replace('$', '') in valid_tickers]

def detect_direction(text):
    text = text.lower()
    long_score = sum(word in text for word in LONG_KEYWORDS)
    short_score = sum(word in text for word in SHORT_KEYWORDS)
    if long_score > short_score:
        return 'long'
    elif short_score > long_score:
        return 'short'
    return 'neutral'
