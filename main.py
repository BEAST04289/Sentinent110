"""
Sentient110 - FastAPI Backend
AI-Powered Financial Sentiment Analysis
"""

import os
import logging
from typing import Optional
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

# Initialize FastAPI
app = FastAPI(
    title="Sentient110",
    description="AI-Powered Financial Sentiment Analysis - Reviving Monitor110",
    version="1.0.0"
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

class AnalysisResponse(BaseModel):
    ticker: str
    signal: str  # BUY, SELL, HOLD
    confidence: float  # 0-100
    reasoning: str
    sentiment_score: float
    sources_analyzed: int
    timestamp: str
    price: Optional[float] = None


# ============= MOCK DATA (for demo) =============

MOCK_ANALYSES = {
    "TSLA": {
        "signal": "BUY",
        "confidence": 89,
        "reasoning": "Strong bullish momentum driven by Cybertruck delivery announcements and multiple analyst upgrades. Twitter sentiment spiked 24 hours ago. Reddit discussions on r/stocks are overwhelmingly positive about upcoming earnings.",
        "sentiment_score": 0.85,
        "sources_analyzed": 156,
        "price": 248.32
    },
    "AAPL": {
        "signal": "HOLD",
        "confidence": 67,
        "reasoning": "Mixed sentiment following iPhone 16 launch. News coverage is positive but social media shows fatigue with incremental updates. Analysts maintain price targets. Wait for Q1 earnings guidance.",
        "sentiment_score": 0.52,
        "sources_analyzed": 203,
        "price": 178.45
    },
    "NVDA": {
        "signal": "BUY",
        "confidence": 94,
        "reasoning": "Extremely bullish sentiment across all sources. AI chip demand continues to exceed expectations. Multiple hedge funds increasing positions. Blackwell architecture receiving universal praise.",
        "sentiment_score": 0.91,
        "sources_analyzed": 187,
        "price": 875.60
    },
    "GME": {
        "signal": "SELL",
        "confidence": 72,
        "reasoning": "Bearish sentiment on fundamentals despite meme activity. Revenue declining, no clear turnaround strategy. Reddit activity nostalgic but not translating to sustained buying pressure.",
        "sentiment_score": 0.28,
        "sources_analyzed": 89,
        "price": 12.34
    },
    "GOOGL": {
        "signal": "BUY",
        "confidence": 78,
        "reasoning": "Positive sentiment around Gemini AI developments. Cloud revenue growth exceeds expectations. Antitrust concerns priced in. Strong buy signals from institutional investors.",
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
    return {"status": "healthy", "service": "Sentient110", "version": "1.0.0"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_ticker(request: AnalysisRequest):
    """
    Analyze sentiment for a stock ticker.
    
    Demo mode: Returns pre-computed results for common tickers.
    Production: Would call RoBERTa + Claude for real analysis.
    """
    ticker = request.ticker.upper().strip()
    
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker symbol required")
    
    logger.info(f"📊 Analyzing {ticker}...")
    
    # Check if we have mock data
    if ticker in MOCK_ANALYSES:
        data = MOCK_ANALYSES[ticker]
    else:
        # Generate random-ish response for unknown tickers
        import random
        signals = ["BUY", "SELL", "HOLD"]
        signal = random.choice(signals)
        confidence = random.randint(50, 95)
        
        data = {
            "signal": signal,
            "confidence": confidence,
            "reasoning": f"Analysis for {ticker}: Based on {random.randint(50, 200)} sources analyzed across news, Twitter, and Reddit. Sentiment trending {'bullish' if signal == 'BUY' else 'bearish' if signal == 'SELL' else 'neutral'}.",
            "sentiment_score": confidence / 100,
            "sources_analyzed": random.randint(50, 200),
            "price": random.uniform(10, 500)
        }
    
    return AnalysisResponse(
        ticker=ticker,
        signal=data["signal"],
        confidence=data["confidence"],
        reasoning=data["reasoning"],
        sentiment_score=data["sentiment_score"],
        sources_analyzed=data["sources_analyzed"],
        timestamp=datetime.now().isoformat(),
        price=data.get("price")
    )


@app.get("/api/trending")
async def get_trending():
    """Get trending tickers with sentiment."""
    return {
        "trending": [
            {"ticker": "TSLA", "signal": "BUY", "confidence": 89},
            {"ticker": "NVDA", "signal": "BUY", "confidence": 94},
            {"ticker": "AAPL", "signal": "HOLD", "confidence": 67},
            {"ticker": "GOOGL", "signal": "BUY", "confidence": 78},
            {"ticker": "GME", "signal": "SELL", "confidence": 72}
        ]
    }


# ============= STARTUP =============

if __name__ == "__main__":
    import uvicorn
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                      SENTIENT110                          ║
    ║       AI-Powered Financial Sentiment Analysis             ║
    ║                                                           ║
    ║  "Every Failure Deserves a Second Run"                    ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="127.0.0.1", port=8000)
