"""
Basic tests for backtest engine (placeholder)
"""
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.market import Candle
from app.models.strategy import StrategyConfig, StrategyType
from app.engines.backtest_engine import BacktestEngine


def test_backtest_engine_basic():
    """Basic backtest engine test"""
    # Create mock candles
    base_time = datetime.now() - timedelta(days=30)
    candles = []
    base_price = 42000.0
    
    for i in range(100):
        price = base_price + (i * 10)  # Simple uptrend
        candles.append(
            Candle(
                timestamp=base_time + timedelta(hours=i),
                open=Decimal(str(price)),
                high=Decimal(str(price + 100)),
                low=Decimal(str(price - 100)),
                close=Decimal(str(price)),
                volume=Decimal("1000"),
                symbol="BTCUSDT",
                timeframe="1h",
            )
        )
    
    # Create strategy config
    strategy_config = StrategyConfig(
        strategy_id="test_strategy",
        strategy_type=StrategyType.MA_CROSSOVER,
        name="Test MA Crossover",
        parameters={
            "short_window": 5,
            "long_window": 10,
        },
    )
    
    # Run backtest
    engine = BacktestEngine(
        initial_capital=Decimal("100000"),
        fee_rate=Decimal("0.001"),
        slippage_rate=Decimal("0.0005"),
    )
    
    result = engine.run([strategy_config], candles)
    
    # Basic assertions
    assert result is not None
    assert result.strategy_id == "test_strategy"
    assert len(result.equity_curve) > 0

