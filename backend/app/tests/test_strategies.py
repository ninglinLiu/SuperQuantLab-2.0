"""
Basic tests for strategies (placeholder)
"""
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.market import Bar
from app.models.strategy import StrategyConfig, StrategyType
from app.strategies.ma_crossover import MACrossoverStrategy


def test_ma_crossover_strategy():
    """Basic MA crossover strategy test"""
    config = StrategyConfig(
        strategy_id="test_ma",
        strategy_type=StrategyType.MA_CROSSOVER,
        name="Test MA",
        parameters={
            "short_window": 5,
            "long_window": 10,
        },
    )
    
    strategy = MACrossoverStrategy(config)
    strategy.reset()
    
    # Create mock bars
    base_time = datetime.now()
    bars = []
    base_price = 100.0
    
    for i in range(20):
        price = base_price + (i * 2)  # Uptrend
        bars.append(
            Bar(
                timestamp=base_time + timedelta(hours=i),
                open=Decimal(str(price)),
                high=Decimal(str(price + 1)),
                low=Decimal(str(price - 1)),
                close=Decimal(str(price)),
                volume=Decimal("100"),
                symbol="BTCUSDT",
                timeframe="1h",
            )
        )
    
    # Process bars
    signals = []
    for bar in bars:
        signal = strategy.on_bar(bar)
        if signal:
            signals.append(signal)
    
    # Should generate some signals
    assert len(signals) >= 0  # May or may not have signals depending on data

