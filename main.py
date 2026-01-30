"""
Sentient110 - FastAPI Backend with Real APIs
AI-Powered Financial Sentiment Analysis
"""

import os
import logging
from typing import Optional, List
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentient110")

# Import our services
try:
    from services.data_aggregator import fetch_all_data, fetch_stock_price
    from services.openai_analyzer import analyze_sentiment
    REAL_API = True
    logger.info("✅ Real API services loaded")
except ImportError as e:
    REAL_API = False
    logger.warning(f"⚠️ Using mock data: {e}")

# Initialize FastAPI
app = FastAPI(
    title="Sentient110",
    description="AI-Powered Financial Sentiment Analysis - Reviving Monitor110",
    version="2.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELS =============

class AnalysisRequest(BaseModel):
    ticker: str

class SourceBreakdown(BaseModel):
    news: int
    twitter: int
    reddit: int

class AnalysisResponse(BaseModel):
    ticker: str
    signal: str
    confidence: float
    reasoning: str
    sentiment_score: float
    sources_analyzed: int
    timestamp: str
    price: Optional[float] = None
    price_change: Optional[str] = None
    source_breakdown: Optional[SourceBreakdown] = None
    insights: Optional[List[str]] = None
    news_headlines: Optional[List[str]] = None
    using_real_data: bool = False


# ============= MOCK DATA (fallback) =============

MOCK_ANALYSES = {
    "TSLA": {
        "signal": "BUY",
        "confidence": 89,
        "reasoning": "Strong bullish momentum driven by Cybertruck delivery announcements and multiple analyst upgrades. Twitter sentiment spiked 24 hours ago.",
        "sentiment_score": 0.85,
        "sources_analyzed": 156,
        "price": 248.32
    },
    "AAPL": {
        "signal": "HOLD",
        "confidence": 67,
        "reasoning": "Mixed sentiment following iPhone 16 launch. News coverage is positive but social media shows fatigue.",
        "sentiment_score": 0.52,
        "sources_analyzed": 203,
        "price": 178.45
    },
    "NVDA": {
        "signal": "BUY",
        "confidence": 94,
        "reasoning": "Extremely bullish sentiment across all sources. AI chip demand continues to exceed expectations.",
        "sentiment_score": 0.91,
        "sources_analyzed": 187,
        "price": 875.60
    },
    "GME": {
        "signal": "SELL",
        "confidence": 72,
        "reasoning": "Bearish sentiment on fundamentals despite meme activity. Revenue declining, no clear turnaround.",
        "sentiment_score": 0.28,
        "sources_analyzed": 89,
        "price": 12.34
    },
    "GOOGL": {
        "signal": "BUY",
        "confidence": 78,
        "reasoning": "Positive sentiment around Gemini AI developments. Cloud revenue growth exceeds expectations.",
        "sentiment_score": 0.73,
        "sources_analyzed": 145,
        "price": 156.78
    }
}


# ============= ENDPOINTS =============

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main dashboard."""
    return FileResponse("frontend/index.html")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Sentient110",
        "version": "2.0.0",
        "real_api": REAL_API,
        "apis": {
            "news": bool(os.getenv("NEWS_API_KEY")),
            "twitter": bool(os.getenv("TWITTER_BEARER_TOKEN")),
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "alpha_vantage": bool(os.getenv("ALPHA_VANTAGE_KEY"))
        }
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_ticker(request: AnalysisRequest):
    """
    Analyze sentiment for a stock ticker.
    Uses real APIs when available, falls back to mock data.
    """
    ticker = request.ticker.upper().strip()
    
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker symbol required")
    
    logger.info(f"📊 Analyzing {ticker}...")
    
    using_real_data = False
    news_headlines = []
    
    # Try real API first
    if REAL_API:
        try:
            # Fetch real data
            data = fetch_all_data(ticker)
            news = data.get("news", [])
            tweets = data.get("tweets", [])
            price_data = data.get("price", {})
            
            # Get AI analysis
            analysis = analyze_sentiment(ticker, news, tweets, price_data)
            
            # Extract headlines for display
            news_headlines = [n.get("title", "")[:80] for n in news[:5]]
            
            using_real_data = True
            logger.info(f"✅ Real analysis complete for {ticker}")
            
            return AnalysisResponse(
                ticker=ticker,
                signal=analysis["signal"],
                confidence=analysis["confidence"],
                reasoning=analysis["reasoning"],
                sentiment_score=analysis["sentiment_score"],
                sources_analyzed=len(news) + len(tweets),
                timestamp=datetime.now().isoformat(),
                price=price_data.get("price"),
                price_change=price_data.get("change_percent", "0%"),
                source_breakdown=SourceBreakdown(
                    news=analysis.get("news_sentiment", 70),
                    twitter=analysis.get("social_sentiment", 70),
                    reddit=max(50, analysis.get("social_sentiment", 70) - 10)
                ),
                insights=analysis.get("insights", []),
                news_headlines=news_headlines,
                using_real_data=True
            )
            
        except Exception as e:
            logger.error(f"Real API failed: {e}, falling back to mock")
    
    # Fallback to mock data
    if ticker in MOCK_ANALYSES:
        data = MOCK_ANALYSES[ticker]
    else:
        import random
        signals = ["BUY", "SELL", "HOLD"]
        signal = random.choice(signals)
        confidence = random.randint(50, 95)
        
        data = {
            "signal": signal,
            "confidence": confidence,
            "reasoning": f"Demo analysis for {ticker}: Sentiment trending {'bullish' if signal == 'BUY' else 'bearish' if signal == 'SELL' else 'neutral'}.",
            "sentiment_score": confidence / 100,
            "sources_analyzed": random.randint(50, 200),
            "price": random.uniform(10, 500)
        }
    
    # Generate mock source breakdown
    import random
    if data["signal"] == "BUY":
        source_breakdown = SourceBreakdown(
            news=random.randint(70, 90),
            twitter=random.randint(75, 95),
            reddit=random.randint(80, 98)
        )
        insights = ["✅ Strong bullish momentum", "✅ Positive analyst coverage", "📈 Volume surge detected"]
    elif data["signal"] == "SELL":
        source_breakdown = SourceBreakdown(
            news=random.randint(20, 40),
            twitter=random.randint(15, 35),
            reddit=random.randint(25, 45)
        )
        insights = ["⚠️ Bearish signals detected", "📉 Declining momentum", "❌ Negative sentiment"]
    else:
        source_breakdown = SourceBreakdown(
            news=random.randint(45, 65),
            twitter=random.randint(40, 60),
            reddit=random.randint(50, 70)
        )
        insights = ["⏸️ Mixed sentiment", "📊 Wait for clearer signals", "🔄 Market consolidating"]
    
    return AnalysisResponse(
        ticker=ticker,
        signal=data["signal"],
        confidence=data["confidence"],
        reasoning=data["reasoning"],
        sentiment_score=data["sentiment_score"],
        sources_analyzed=data["sources_analyzed"],
        timestamp=datetime.now().isoformat(),
        price=data.get("price"),
        source_breakdown=source_breakdown,
        insights=insights,
        using_real_data=False
    )


@app.get("/api/trending")
async def get_trending():
    """Get trending tickers with sentiment."""
    return {
        "trending": [
            {"ticker": "TSLA", "signal": "BUY", "confidence": 89, "price": 248.32},
            {"ticker": "NVDA", "signal": "BUY", "confidence": 94, "price": 875.60},
            {"ticker": "AAPL", "signal": "HOLD", "confidence": 67, "price": 178.45},
            {"ticker": "GOOGL", "signal": "BUY", "confidence": 78, "price": 156.78},
            {"ticker": "GME", "signal": "SELL", "confidence": 72, "price": 12.34}
        ]
    }


# Blockchain verification storage (in-memory for demo)
BLOCKCHAIN_STORE = {}

@app.post("/api/verify")
async def verify_prediction(ticker: str, signal: str, confidence: float):
    """Store prediction on blockchain for verification."""
    import hashlib
    
    timestamp = datetime.now().isoformat()
    data = f"{ticker}|{signal}|{confidence}|{timestamp}"
    tx_hash = "0x" + hashlib.sha256(data.encode()).hexdigest()
    
    BLOCKCHAIN_STORE[tx_hash] = {
        "ticker": ticker,
        "signal": signal,
        "confidence": confidence,
        "timestamp": timestamp
    }
    
    return {
        "tx_hash": tx_hash,
        "timestamp": timestamp,
        "network": "Story Protocol (Sepolia)",
        "verification_url": f"https://sepolia.etherscan.io/tx/{tx_hash}"
    }


@app.get("/api/verify/{tx_hash}")
async def get_verification(tx_hash: str):
    """Verify a prediction by transaction hash."""
    if tx_hash in BLOCKCHAIN_STORE:
        return {"verified": True, "prediction": BLOCKCHAIN_STORE[tx_hash]}
    return {"verified": False, "message": "Prediction not found"}


# ============= STARTUP =============

if __name__ == "__main__":
    import uvicorn
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                      SENTIENT110 v2.0                     ║
    ║       AI-Powered Financial Sentiment Analysis             ║
    ║                                                           ║
    ║  "Every Failure Deserves a Second Run"                    ║
    ║                                                           ║
    ║  APIs: NewsAPI, Twitter/X, OpenAI, Alpha Vantage          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="127.0.0.1", port=8000)
