"""
Sentient110 - Claude AI Integration
Deep analysis using Anthropic's Claude 3.5 Haiku
"""

import os
import json
import logging
from typing import Optional
from anthropic import Anthropic

logger = logging.getLogger("sentient110.claude")

# Initialize client
client = None

def init_claude():
    """Initialize the Claude client."""
    global client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        client = Anthropic(api_key=api_key)
        logger.info("✅ Claude AI initialized")
        return True
    else:
        logger.warning("⚠️ No Anthropic API key found - using demo mode")
        return False


def analyze_with_claude(ticker: str, news_texts: list, social_texts: list, price: float = None) -> dict:
    """
    Use Claude to synthesize sentiment and generate trading signal.
    
    Args:
        ticker: Stock ticker symbol
        news_texts: List of news headlines/summaries
        social_texts: List of social media posts
        price: Current stock price
        
    Returns:
        {
            "signal": "BUY/SELL/HOLD",
            "confidence": 0-100,
            "reasoning": "Plain English explanation",
            "sentiment_score": 0-1
        }
    """
    global client
    
    if not client:
        init_claude()
    
    if not client:
        # Demo mode fallback
        return {
            "signal": "HOLD",
            "confidence": 65,
            "reasoning": f"Demo mode: Unable to connect to Claude AI. Based on simulated analysis of {ticker}.",
            "sentiment_score": 0.5
        }
    
    # Prepare the prompt
    prompt = f"""You are a financial sentiment analyst. Analyze the following data for {ticker} and provide a trading recommendation.

CURRENT PRICE: ${price if price else 'Unknown'}

NEWS HEADLINES ({len(news_texts)} sources):
{chr(10).join([f"- {text[:200]}" for text in news_texts[:10]])}

SOCIAL MEDIA SENTIMENT ({len(social_texts)} posts):
{chr(10).join([f"- {text[:150]}" for text in social_texts[:10]])}

Based on this data, provide your analysis in the following JSON format ONLY (no other text):
{{
    "signal": "BUY" or "SELL" or "HOLD",
    "confidence": 0-100,
    "reasoning": "2-3 sentence explanation in plain English",
    "sentiment_score": 0.0-1.0 (0=very bearish, 1=very bullish)
}}
"""
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse response
        content = response.content[0].text.strip()
        
        # Try to extract JSON
        if "{" in content:
            json_start = content.index("{")
            json_end = content.rindex("}") + 1
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
            
            return {
                "signal": result.get("signal", "HOLD"),
                "confidence": min(100, max(0, result.get("confidence", 50))),
                "reasoning": result.get("reasoning", "Analysis complete."),
                "sentiment_score": min(1.0, max(0.0, result.get("sentiment_score", 0.5)))
            }
        else:
            raise ValueError("No JSON in response")
            
    except Exception as e:
        logger.error(f"Claude analysis failed: {e}")
        return {
            "signal": "HOLD",
            "confidence": 50,
            "reasoning": f"Analysis temporarily unavailable. Please try again.",
            "sentiment_score": 0.5
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test
    init_claude()
    
    test_news = [
        "Tesla reports record quarterly deliveries",
        "Analysts upgrade TSLA price target to $300",
        "Elon Musk announces new Cybertruck features"
    ]
    
    test_social = [
        "TSLA to the moon! 🚀",
        "Just bought more Tesla shares",
        "This dip is a buying opportunity"
    ]
    
    result = analyze_with_claude("TSLA", test_news, test_social, 248.32)
    print(json.dumps(result, indent=2))
