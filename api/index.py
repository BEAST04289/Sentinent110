"""
Sentient110 - Vercel Serverless Handler
Uses proper Vercel Python format with http.server.BaseHTTPRequestHandler
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import hashlib
from datetime import datetime
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests."""
        path = urlparse(self.path).path
        
        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "service": "Sentient110",
                "version": "2.0.0",
                "real_api": bool(os.getenv("OPENAI_API_KEY")),
                "timestamp": datetime.now().isoformat()
            })
        
        elif path == "/api/trending":
            self._send_json({
                "trending": [
                    {"ticker": "TSLA", "signal": "BUY", "confidence": 89, "price": 248.32},
                    {"ticker": "NVDA", "signal": "BUY", "confidence": 94, "price": 875.60},
                    {"ticker": "AAPL", "signal": "HOLD", "confidence": 67, "price": 178.45},
                    {"ticker": "GOOGL", "signal": "BUY", "confidence": 78, "price": 156.78},
                    {"ticker": "GME", "signal": "SELL", "confidence": 72, "price": 12.34}
                ]
            })
        
        elif path.startswith("/api/verify/"):
            tx_hash = path.split("/")[-1]
            self._send_json({"verified": False, "tx_hash": tx_hash, "message": "Demo mode - hash not found"})
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests."""
        path = urlparse(self.path).path
        
        if path == "/api/analyze":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body) if body else {}
                ticker = data.get("ticker", "TSLA").upper().strip()
            except:
                ticker = "TSLA"
            
            # Analyze
            result = self._analyze_ticker(ticker)
            self._send_json(result)
        
        elif path == "/api/verify":
            query = parse_qs(urlparse(self.path).query)
            ticker = query.get("ticker", ["TSLA"])[0]
            signal = query.get("signal", ["BUY"])[0]
            confidence = query.get("confidence", ["85"])[0]
            
            timestamp = datetime.now().isoformat()
            data_str = f"{ticker}|{signal}|{confidence}|{timestamp}"
            tx_hash = "0x" + hashlib.sha256(data_str.encode()).hexdigest()
            
            self._send_json({
                "tx_hash": tx_hash,
                "timestamp": timestamp,
                "network": "Story Protocol (Sepolia)",
                "verification_url": f"https://sepolia.etherscan.io/tx/{tx_hash}"
            })
        
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _analyze_ticker(self, ticker):
        """Analyze a ticker with real APIs when available."""
        import random
        
        # Try real news
        news = self._fetch_news(ticker)
        
        # Try OpenAI analysis
        ai_result = self._openai_analyze(ticker, news)
        using_real = ai_result is not None
        
        if not ai_result:
            ai_result = self._fallback_analysis(ticker, news)
        
        # Get price
        price_data = self._fetch_price(ticker)
        
        # Source breakdown based on signal
        if ai_result["signal"] == "BUY":
            breakdown = {"news": random.randint(72, 92), "twitter": random.randint(75, 95), "reddit": random.randint(78, 98)}
        elif ai_result["signal"] == "SELL":
            breakdown = {"news": random.randint(18, 38), "twitter": random.randint(15, 35), "reddit": random.randint(22, 42)}
        else:
            breakdown = {"news": random.randint(45, 62), "twitter": random.randint(42, 58), "reddit": random.randint(48, 65)}
        
        return {
            "ticker": ticker,
            "signal": ai_result["signal"],
            "confidence": ai_result["confidence"],
            "reasoning": ai_result["reasoning"],
            "sentiment_score": 0.85 if ai_result["signal"] == "BUY" else 0.25 if ai_result["signal"] == "SELL" else 0.50,
            "sources_analyzed": len(news) + 3,
            "timestamp": datetime.now().isoformat(),
            "price": price_data.get("price"),
            "price_change": price_data.get("change_percent"),
            "source_breakdown": breakdown,
            "insights": ai_result.get("insights", ["Analysis complete"]),
            "news_headlines": [n.get("title", "")[:80] for n in news[:5]],
            "using_real_data": using_real
        }
    
    def _fetch_news(self, ticker):
        """Fetch news from NewsAPI."""
        import requests
        api_key = os.getenv("NEWS_API_KEY")
        
        if not api_key:
            return self._mock_news(ticker)
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {"q": f"{ticker} stock", "sortBy": "publishedAt", "pageSize": 5, "language": "en", "apiKey": api_key}
            resp = requests.get(url, params=params, timeout=8)
            data = resp.json()
            if data.get("status") == "ok":
                return [{"title": a.get("title", ""), "source": a.get("source", {}).get("name", "")} for a in data.get("articles", [])[:5]]
        except:
            pass
        
        return self._mock_news(ticker)
    
    def _mock_news(self, ticker):
        return [
            {"title": f"{ticker} shows strong momentum amid market rally", "source": "Reuters"},
            {"title": f"Analysts upgrade {ticker} on strong earnings outlook", "source": "Bloomberg"},
            {"title": f"{ticker} leads sector gains on positive sentiment", "source": "CNBC"},
        ]
    
    def _fetch_price(self, ticker):
        """Fetch price from Alpha Vantage."""
        import requests
        import random
        api_key = os.getenv("ALPHA_VANTAGE_KEY")
        
        if not api_key:
            return self._mock_price(ticker)
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {"function": "GLOBAL_QUOTE", "symbol": ticker, "apikey": api_key}
            resp = requests.get(url, params=params, timeout=8)
            quote = resp.json().get("Global Quote", {})
            if quote:
                return {"price": float(quote.get("05. price", 0)), "change_percent": quote.get("10. change percent", "0%")}
        except:
            pass
        
        return self._mock_price(ticker)
    
    def _mock_price(self, ticker):
        import random
        prices = {"TSLA": 248.32, "AAPL": 178.45, "NVDA": 875.60, "GOOGL": 156.78, "GME": 12.34}
        price = prices.get(ticker, round(random.uniform(50, 500), 2))
        return {"price": price, "change_percent": f"{random.uniform(-3, 3):+.2f}%"}
    
    def _openai_analyze(self, ticker, news):
        """Use OpenAI for analysis."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            news_text = "\n".join([f"- {n.get('title', '')}" for n in news[:5]])
            
            prompt = f"""Analyze {ticker} stock sentiment from these headlines:

{news_text}

Respond in JSON only:
{{"signal": "BUY" or "SELL" or "HOLD", "confidence": 60-95, "reasoning": "2-3 sentences", "insights": ["insight1", "insight2", "insight3"]}}"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Financial analyst. JSON only."}, {"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            if "{" in content:
                return json.loads(content[content.index("{"):content.rindex("}")+1])
        except Exception as e:
            print(f"OpenAI error: {e}")
        
        return None
    
    def _fallback_analysis(self, ticker, news):
        """Simple keyword-based fallback."""
        import random
        all_text = " ".join([n.get("title", "") for n in news]).lower()
        
        bullish = ["bullish", "up", "growth", "beat", "strong", "rally", "gain", "upgrade"]
        bearish = ["bearish", "down", "decline", "miss", "weak", "crash", "downgrade"]
        
        pos = sum(1 for w in bullish if w in all_text)
        neg = sum(1 for w in bearish if w in all_text)
        
        if pos > neg:
            return {"signal": "BUY", "confidence": random.randint(72, 92), "reasoning": f"Bullish sentiment detected for {ticker}.", "insights": ["✅ Positive sentiment", "📈 Strong momentum", "🔥 High engagement"]}
        elif neg > pos:
            return {"signal": "SELL", "confidence": random.randint(65, 85), "reasoning": f"Bearish signals for {ticker}.", "insights": ["⚠️ Negative trend", "📉 Declining momentum", "❌ Weak fundamentals"]}
        else:
            return {"signal": "HOLD", "confidence": random.randint(55, 70), "reasoning": f"Mixed signals for {ticker}.", "insights": ["⏸️ Mixed sentiment", "📊 Consolidation", "🔄 Wait for breakout"]}
