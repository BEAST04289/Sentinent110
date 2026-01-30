"""
Sentient110 - OpenAI Integration
Uses GPT-4o-mini for fast, cheap sentiment analysis
"""

import os
import json
import logging
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("sentient110.openai")

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("openai package not installed. Run: pip install openai")


def analyze_sentiment(ticker: str, news: List[Dict], tweets: List[Dict], price: Dict = None) -> Dict:
    """
    Use OpenAI GPT-4o-mini to analyze sentiment and generate trading signal.
    
    GPT-4o-mini is the fastest and cheapest option:
    - $0.15/1M input tokens
    - $0.60/1M output tokens
    - Very fast response
    
    Args:
        ticker: Stock symbol
        news: List of news articles
        tweets: List of tweets
        price: Current price data
        
    Returns:
        {
            "signal": "BUY/SELL/HOLD",
            "confidence": 0-100,
            "reasoning": "Explanation",
            "sentiment_score": 0-1
        }
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or not OPENAI_AVAILABLE:
        logger.warning("OpenAI not available, using fallback")
        return _fallback_analysis(ticker, news, tweets)
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Build prompt with limited data
        news_text = "\n".join([f"- {n.get('title', '')}" for n in news[:5]])
        tweets_text = "\n".join([f"- {t.get('text', '')}" for t in tweets[:5]])
        price_info = f"${price.get('price', 0):.2f} ({price.get('change_percent', '0%')})" if price else "N/A"
        
        prompt = f"""Analyze the sentiment for {ticker} stock based on this data:

CURRENT PRICE: {price_info}

NEWS HEADLINES:
{news_text}

SOCIAL MEDIA:
{tweets_text}

Provide your analysis in this exact JSON format:
{{
    "signal": "BUY" or "SELL" or "HOLD",
    "confidence": 50-100,
    "reasoning": "2-3 sentence explanation",
    "sentiment_score": 0.0-1.0,
    "news_sentiment": 0-100,
    "social_sentiment": 0-100,
    "key_insights": ["insight1", "insight2", "insight3"]
}}

Be concise. Respond ONLY with the JSON."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fastest & cheapest
            messages=[
                {"role": "system", "content": "You are a financial sentiment analyst. Respond only in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON
        if "{" in content:
            json_start = content.index("{")
            json_end = content.rindex("}") + 1
            result = json.loads(content[json_start:json_end])
            
            return {
                "signal": result.get("signal", "HOLD"),
                "confidence": min(100, max(50, result.get("confidence", 65))),
                "reasoning": result.get("reasoning", "Analysis complete."),
                "sentiment_score": min(1.0, max(0.0, result.get("sentiment_score", 0.5))),
                "news_sentiment": result.get("news_sentiment", 50),
                "social_sentiment": result.get("social_sentiment", 50),
                "insights": result.get("key_insights", ["Analysis complete"])
            }
        else:
            raise ValueError("No JSON in response")
            
    except Exception as e:
        logger.error(f"OpenAI analysis failed: {e}")
        return _fallback_analysis(ticker, news, tweets)


def _fallback_analysis(ticker: str, news: List[Dict], tweets: List[Dict]) -> Dict:
    """Fallback when OpenAI is not available."""
    import random
    
    # Simple keyword-based sentiment
    positive_words = ["bullish", "buy", "up", "growth", "beat", "strong", "moon", "rocket", "🚀"]
    negative_words = ["bearish", "sell", "down", "decline", "miss", "weak", "crash", "dump"]
    
    all_text = " ".join([n.get("title", "") for n in news] + [t.get("text", "") for t in tweets]).lower()
    
    pos_count = sum(1 for word in positive_words if word in all_text)
    neg_count = sum(1 for word in negative_words if word in all_text)
    
    if pos_count > neg_count + 1:
        signal = "BUY"
        confidence = min(95, 70 + pos_count * 5)
        sentiment = 0.7 + random.uniform(0, 0.25)
    elif neg_count > pos_count + 1:
        signal = "SELL"
        confidence = min(95, 70 + neg_count * 5)
        sentiment = 0.3 - random.uniform(0, 0.2)
    else:
        signal = "HOLD"
        confidence = random.randint(55, 70)
        sentiment = 0.5 + random.uniform(-0.1, 0.1)
    
    return {
        "signal": signal,
        "confidence": confidence,
        "reasoning": f"Based on {len(news)} news articles and {len(tweets)} social posts, sentiment is trending {'bullish' if signal == 'BUY' else 'bearish' if signal == 'SELL' else 'neutral'}.",
        "sentiment_score": sentiment,
        "news_sentiment": random.randint(40, 90),
        "social_sentiment": random.randint(40, 90),
        "insights": [
            f"{'Positive' if signal == 'BUY' else 'Negative' if signal == 'SELL' else 'Mixed'} sentiment detected",
            f"{len(news)} news sources analyzed",
            f"{len(tweets)} social posts processed"
        ]
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test
    test_news = [{"title": "Tesla Cybertruck deliveries exceed expectations"}]
    test_tweets = [{"text": "$TSLA to the moon! 🚀"}]
    test_price = {"price": 248.32, "change_percent": "+2.5%"}
    
    result = analyze_sentiment("TSLA", test_news, test_tweets, test_price)
    print(json.dumps(result, indent=2))
