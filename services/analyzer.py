"""
Sentient110 - RoBERTa Sentiment Analyzer
Fast local sentiment analysis using HuggingFace transformers
"""

import logging
from typing import List, Dict, Optional
from transformers import pipeline

logger = logging.getLogger("sentient110.analyzer")


class SentimentAnalyzer:
    """
    RoBERTa-based sentiment analyzer for financial text.
    Uses cardiffnlp/twitter-roberta-base-sentiment model.
    """
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the RoBERTa sentiment model."""
        try:
            logger.info("🧠 Loading RoBERTa sentiment model...")
            self.model = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment"
            )
            logger.info("✅ Model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.model = None
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Text to analyze
            
        Returns:
            {"label": "positive/negative/neutral", "score": 0-1}
        """
        if not self.model:
            return {"label": "neutral", "score": 0.5}
        
        try:
            # Truncate long text
            text = text[:512]
            result = self.model(text)[0]
            
            # Map labels
            label_map = {
                "LABEL_0": "negative",
                "LABEL_1": "neutral", 
                "LABEL_2": "positive"
            }
            
            return {
                "label": label_map.get(result["label"], result["label"]),
                "score": result["score"]
            }
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {"label": "neutral", "score": 0.5}
    
    def analyze_batch(self, texts: List[str]) -> Dict:
        """
        Analyze sentiment of multiple texts and aggregate.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            {
                "positive": 0-1,
                "negative": 0-1,
                "neutral": 0-1,
                "score": 0-1 (overall bullishness)
            }
        """
        if not texts:
            return {"positive": 0.33, "negative": 0.33, "neutral": 0.34, "score": 0.5}
        
        counts = {"positive": 0, "negative": 0, "neutral": 0}
        weighted_score = 0
        
        for text in texts[:50]:  # Limit for performance
            result = self.analyze_text(text)
            label = result["label"]
            score = result["score"]
            
            counts[label] = counts.get(label, 0) + 1
            
            if label == "positive":
                weighted_score += score
            elif label == "negative":
                weighted_score -= score
        
        total = len(texts[:50])
        
        return {
            "positive": counts["positive"] / total,
            "negative": counts["negative"] / total,
            "neutral": counts["neutral"] / total,
            "score": (weighted_score / total + 1) / 2  # Normalize to 0-1
        }
    
    def get_signal(self, texts: List[str]) -> str:
        """
        Get BUY/SELL/HOLD signal from texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            "BUY", "SELL", or "HOLD"
        """
        result = self.analyze_batch(texts)
        
        if result["positive"] > 0.6:
            return "BUY"
        elif result["negative"] > 0.6:
            return "SELL"
        else:
            return "HOLD"


def analyze_sentiment(texts: List[str]) -> Dict:
    """Convenience function."""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_batch(texts)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "TSLA to the moon! 🚀 Best investment ever",
        "Tesla is overvalued, I'm selling everything",
        "Holding my position, waiting for earnings",
        "This dip is tasty, buying more shares",
        "Bearish on the whole market right now"
    ]
    
    print("\n=== Testing Sentiment Analyzer ===")
    for text in test_texts:
        result = analyzer.analyze_text(text)
        print(f"{result['label'].upper()} ({result['score']:.2f}): {text[:50]}")
    
    print("\n=== Aggregate Results ===")
    agg = analyzer.analyze_batch(test_texts)
    print(f"Positive: {agg['positive']:.1%}")
    print(f"Negative: {agg['negative']:.1%}")
    print(f"Neutral: {agg['neutral']:.1%}")
    print(f"Overall Score: {agg['score']:.2f}")
    print(f"Signal: {analyzer.get_signal(test_texts)}")
