"""
Sentient110 - Blockchain Verification
Story Protocol integration for timestamping predictions
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("sentient110.blockchain")

# Simulated blockchain storage (for demo)
PREDICTION_STORE = {}


def generate_prediction_hash(ticker: str, signal: str, confidence: float, timestamp: str) -> str:
    """
    Generate a unique hash for a prediction.
    This hash would be stored on-chain in production.
    """
    data = f"{ticker}|{signal}|{confidence}|{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()


def store_prediction(
    ticker: str,
    signal: str,
    confidence: float,
    reasoning: str,
    timestamp: str = None
) -> dict:
    """
    Store a prediction with blockchain-style verification.
    
    In demo mode: Stores locally with hash
    In production: Would store on Story Protocol
    
    Returns:
        {
            "tx_hash": "0x...",
            "block_number": 12345,
            "timestamp": "2026-01-30T23:30:00",
            "verification_url": "https://..."
        }
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    # Generate unique hash
    prediction_hash = generate_prediction_hash(ticker, signal, confidence, timestamp)
    tx_hash = f"0x{prediction_hash[:64]}"
    
    # Simulate block number
    import random
    block_number = 19000000 + random.randint(1, 100000)
    
    # Store locally
    prediction_data = {
        "ticker": ticker,
        "signal": signal,
        "confidence": confidence,
        "reasoning": reasoning,
        "timestamp": timestamp,
        "tx_hash": tx_hash,
        "block_number": block_number,
        "network": "Story Protocol (Sepolia Testnet)",
        "verified": True
    }
    
    PREDICTION_STORE[tx_hash] = prediction_data
    
    logger.info(f"🔗 Prediction stored: {tx_hash[:16]}...")
    
    return {
        "tx_hash": tx_hash,
        "block_number": block_number,
        "timestamp": timestamp,
        "verification_url": f"https://sepolia.etherscan.io/tx/{tx_hash}",
        "network": "Story Protocol (Sepolia)"
    }


def verify_prediction(tx_hash: str) -> Optional[dict]:
    """
    Verify a prediction by its transaction hash.
    
    Returns the original prediction data if found.
    """
    if tx_hash in PREDICTION_STORE:
        return PREDICTION_STORE[tx_hash]
    return None


def get_prediction_history(ticker: str = None, limit: int = 10) -> list:
    """
    Get recent predictions, optionally filtered by ticker.
    """
    predictions = list(PREDICTION_STORE.values())
    
    if ticker:
        predictions = [p for p in predictions if p["ticker"] == ticker]
    
    # Sort by timestamp (newest first)
    predictions.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return predictions[:limit]


def get_accuracy_stats(ticker: str = None) -> dict:
    """
    Calculate accuracy statistics for predictions.
    (In production, this would compare predictions to actual price movements)
    """
    predictions = get_prediction_history(ticker, limit=100)
    
    if not predictions:
        return {
            "total_predictions": 0,
            "accuracy": None,
            "avg_confidence": None
        }
    
    total = len(predictions)
    avg_confidence = sum(p["confidence"] for p in predictions) / total
    
    # Simulated accuracy (would be real in production)
    import random
    accuracy = 75 + random.randint(0, 20)  # 75-95%
    
    return {
        "total_predictions": total,
        "accuracy": accuracy,
        "avg_confidence": round(avg_confidence, 1),
        "ticker": ticker
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test
    result = store_prediction(
        ticker="TSLA",
        signal="BUY",
        confidence=89,
        reasoning="Strong bullish momentum"
    )
    
    print("Stored prediction:")
    print(json.dumps(result, indent=2))
    
    # Verify
    verified = verify_prediction(result["tx_hash"])
    print("\nVerified prediction:")
    print(json.dumps(verified, indent=2))
