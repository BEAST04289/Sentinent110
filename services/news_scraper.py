"""
Sentient110 - Financial News Scraper
Fetches mainstream financial news using NewsAPI
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("sentient110.news")

try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    logger.warning("newsapi-python not installed. Run: pip install newsapi-python")


class NewsScraper:
    """Fetches financial news from NewsAPI for stock sentiment analysis."""
    
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.enabled = bool(self.api_key) and NEWSAPI_AVAILABLE
        
        if self.enabled:
            self.client = NewsApiClient(api_key=self.api_key)
            logger.info("✅ NewsAPI: Initialized")
        else:
            self.client = None
            if not self.api_key:
                logger.warning("⚠️ NEWS_API_KEY not found")
    
    def fetch_financial_news(
        self, 
        ticker: str, 
        max_results: int = 20,
        days_back: int = 1
    ) -> List[Dict]:
        """
        Fetch recent financial news for a stock ticker.
        
        Args:
            ticker: Stock symbol (e.g., "AAPL", "TSLA")
            max_results: Maximum articles to return
            days_back: Days to look back
            
        Returns:
            List of article dicts
        """
        if not self.enabled:
            return self._get_mock_news(ticker)
        
        try:
            query = f'"{ticker}" OR "{ticker} stock"'
            from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            logger.info(f"📰 Fetching news for: {ticker}")
            
            response = self.client.get_everything(
                q=query,
                language='en',
                sort_by='publishedAt',
                from_param=from_date,
                page_size=min(max_results, 100)
            )
            
            articles = response.get("articles", [])
            
            if not articles:
                return self._get_mock_news(ticker)
            
            result = []
            for article in articles[:max_results]:
                result.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "url": article.get("url", ""),
                    "published_at": article.get("publishedAt", "")
                })
            
            logger.info(f"✅ Found {len(result)} articles")
            return result
            
        except Exception as e:
            logger.error(f"❌ NewsAPI error: {e}")
            return self._get_mock_news(ticker)
    
    def _get_mock_news(self, ticker: str) -> List[Dict]:
        """Return mock news for demo purposes."""
        return [
            {"title": f"{ticker} shows strong momentum in today's trading", "source": "Reuters", "description": "Market analysts bullish on outlook"},
            {"title": f"Analysts upgrade {ticker} price target", "source": "Bloomberg", "description": "New innovations drive positive sentiment"},
            {"title": f"{ticker} beats quarterly earnings expectations", "source": "CNBC", "description": "Revenue growth exceeds forecasts"}
        ]
    
    def get_headlines_text(self, ticker: str, max_headlines: int = 10) -> str:
        """Get headlines as formatted text for LLM prompts."""
        articles = self.fetch_financial_news(ticker, max_results=max_headlines)
        
        if not articles:
            return f"No news found for {ticker}"
        
        headlines = []
        for i, article in enumerate(articles, 1):
            source = article.get("source", "Unknown")
            title = article.get("title", "No title")
            headlines.append(f"{i}. [{source}] {title}")
        
        return "\n".join(headlines)


def fetch_financial_news(ticker: str, count: int = 20) -> List[Dict]:
    """Convenience function."""
    scraper = NewsScraper()
    return scraper.fetch_financial_news(ticker, max_results=count)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = NewsScraper()
    
    print("\n=== Testing NewsAPI for TSLA ===")
    news = scraper.fetch_financial_news("TSLA", max_results=5)
    for article in news:
        print(f"📰 {article['source']}: {article['title']}")
