"""
Sentient110 - Real Data Aggregator
Fetches real data from NewsAPI, Twitter, Alpha Vantage with rate limiting and fallbacks
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()
logger = logging.getLogger("sentient110.data")

# Rate limits
MAX_NEWS = int(os.getenv("MAX_NEWS_PER_REQUEST", 5))
MAX_TWEETS = int(os.getenv("MAX_TWEETS_PER_REQUEST", 5))

# ============= NEWS API =============

def fetch_news(ticker: str, limit: int = 5) -> List[Dict]:
    """Fetch news from NewsAPI with fallback."""
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        logger.warning("No NEWS_API_KEY, using fallback")
        return _mock_news(ticker)
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f"{ticker} stock",
            "sortBy": "publishedAt",
            "pageSize": min(limit, MAX_NEWS),
            "language": "en",
            "apiKey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") != "ok":
            logger.error(f"NewsAPI error: {data.get('message')}")
            return _mock_news(ticker)
        
        articles = data.get("articles", [])[:limit]
        
        return [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "source": a.get("source", {}).get("name", "Unknown"),
                "url": a.get("url", ""),
                "published": a.get("publishedAt", "")
            }
            for a in articles
        ]
        
    except Exception as e:
        logger.error(f"NewsAPI failed: {e}")
        return _mock_news(ticker)


def _mock_news(ticker: str) -> List[Dict]:
    """Fallback mock news."""
    return [
        {"title": f"{ticker} shows strong momentum today", "source": "Reuters", "description": "Analysts bullish"},
        {"title": f"{ticker} earnings beat expectations", "source": "Bloomberg", "description": "Revenue up 15%"},
        {"title": f"Why {ticker} is trending on Wall Street", "source": "CNBC", "description": "Institutional buying"},
    ]


# ============= TWITTER/X API =============

def fetch_tweets(ticker: str, limit: int = 5) -> List[Dict]:
    """Fetch tweets about a stock with fallback."""
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not bearer_token:
        logger.warning("No TWITTER_BEARER_TOKEN, using fallback")
        return _mock_tweets(ticker)
    
    try:
        # URL decode the token if needed
        import urllib.parse
        bearer_token = urllib.parse.unquote(bearer_token)
        
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {bearer_token}"}
        params = {
            "query": f"${ticker} stock -is:retweet lang:en",
            "max_results": min(limit, MAX_TWEETS, 10),
            "tweet.fields": "created_at,public_metrics"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        
        if "data" not in data:
            logger.warning(f"Twitter returned no data: {data}")
            return _mock_tweets(ticker)
        
        tweets = data.get("data", [])[:limit]
        
        return [
            {
                "text": t.get("text", ""),
                "created_at": t.get("created_at", ""),
                "likes": t.get("public_metrics", {}).get("like_count", 0)
            }
            for t in tweets
        ]
        
    except Exception as e:
        logger.error(f"Twitter API failed: {e}")
        return _mock_tweets(ticker)


def _mock_tweets(ticker: str) -> List[Dict]:
    """Fallback mock tweets."""
    return [
        {"text": f"${ticker} looking bullish! 🚀", "likes": 150},
        {"text": f"Just added more ${ticker} to my portfolio", "likes": 89},
        {"text": f"${ticker} earnings coming up, expecting good results", "likes": 245},
    ]


# ============= ALPHA VANTAGE (Stock Prices) =============

def fetch_stock_price(ticker: str) -> Optional[Dict]:
    """Fetch real-time stock price from Alpha Vantage."""
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    
    if not api_key:
        logger.warning("No ALPHA_VANTAGE_KEY, using fallback")
        return _mock_price(ticker)
    
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        quote = data.get("Global Quote", {})
        
        if not quote:
            return _mock_price(ticker)
        
        return {
            "symbol": quote.get("01. symbol", ticker),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%"),
            "volume": int(quote.get("06. volume", 0))
        }
        
    except Exception as e:
        logger.error(f"Alpha Vantage failed: {e}")
        return _mock_price(ticker)


def _mock_price(ticker: str) -> Dict:
    """Fallback mock price."""
    import random
    prices = {"TSLA": 248.32, "AAPL": 178.45, "NVDA": 875.60, "GOOGL": 156.78, "GME": 12.34}
    price = prices.get(ticker, random.uniform(50, 500))
    return {
        "symbol": ticker,
        "price": price,
        "change": random.uniform(-5, 5),
        "change_percent": f"{random.uniform(-3, 3):.2f}%",
        "volume": random.randint(1000000, 50000000)
    }


# ============= AGGREGATE ALL DATA =============

def fetch_all_data(ticker: str) -> Dict:
    """Aggregate data from all sources."""
    logger.info(f"📡 Fetching data for {ticker}...")
    
    news = fetch_news(ticker, limit=5)
    tweets = fetch_tweets(ticker, limit=5)
    price_data = fetch_stock_price(ticker)
    
    return {
        "ticker": ticker,
        "news": news,
        "tweets": tweets,
        "price": price_data,
        "sources_count": len(news) + len(tweets),
        "fetched_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\n=== Testing Data Aggregator ===")
    data = fetch_all_data("TSLA")
    
    print(f"\n📰 News ({len(data['news'])} articles):")
    for n in data['news']:
        print(f"  - {n['source']}: {n['title'][:50]}...")
    
    print(f"\n🐦 Tweets ({len(data['tweets'])}):")
    for t in data['tweets']:
        print(f"  - {t['text'][:50]}...")
    
    print(f"\n💰 Price: ${data['price']['price']:.2f}")
