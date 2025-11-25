"""
Basic tests for chaos engine (placeholder)
"""
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.market import Candle
from app.engines.chaos_engine import ChaosEngine


def test_chaos_engine():
    """Basic chaos engine test"""
    engine = ChaosEngine()
    
    # Create mock candles
    base_time = datetime.now()
    candles = []
    base_price = 100.0
    
    for i in range(200):
        # Add some noise
        import random
        price = base_price + (i * 0.1) + random.uniform(-2, 2)
        candles.append(
            Candle(
                timestamp=base_time + timedelta(hours=i),
                open=Decimal(str(price)),
                high=Decimal(str(price + 1)),
                low=Decimal(str(price - 1)),
                close=Decimal(str(price)),
                volume=Decimal("1000"),
                symbol="BTCUSDT",
                timeframe="1h",
            )
        )
    
    # Calculate chaos index
    chaos_index = engine.calculate_chaos_index(candles, window=100)
    
    # Should return a value between 0 and 1
    assert 0 <= chaos_index <= 1

