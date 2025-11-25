"""
Demo/Mock data for frontend demonstration
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List
import random

from app.models.market import Candle, Trade, Signal, Side
from app.models.strategy import RegimeState
from app.engines.behavior_engine import BehaviorMetrics


def generate_demo_candles(
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    days: int = 30,
) -> List[Candle]:
    """
    Generate demo candle data for testing.
    
    Args:
        symbol: Trading pair symbol
        timeframe: Timeframe
        days: Number of days of data
    
    Returns:
        List of Candle objects
    """
    candles = []
    base_time = datetime.now() - timedelta(days=days)
    base_price = 42000.0
    
    # Generate price trend with some randomness
    current_price = base_price
    trend = 0.001  # Slight upward trend
    
    for i in range(days * 24):  # Hourly data
        # Add trend and random walk
        change = random.uniform(-200, 300) * trend + random.gauss(0, 100)
        current_price = max(30000, min(60000, current_price + change))
        
        high = current_price + random.uniform(50, 200)
        low = current_price - random.uniform(50, 200)
        volume = random.uniform(500, 3000)
        
        candle = Candle(
            timestamp=base_time + timedelta(hours=i),
            open=Decimal(str(current_price)),
            high=Decimal(str(high)),
            low=Decimal(str(low)),
            close=Decimal(str(current_price)),
            volume=Decimal(str(volume)),
            symbol=symbol,
            timeframe=timeframe,
        )
        candles.append(candle)
        
        # Update price for next candle
        current_price = float(candle.close)
    
    return candles


def generate_demo_behavior_metrics() -> BehaviorMetrics:
    """Generate demo behavior metrics"""
    return BehaviorMetrics(
        impulsiveness_index=0.45,  # Moderate impulsiveness
        chase_selloff_index=0.32,  # Low chase-selloff
        consecutive_losses=2,  # 2 consecutive losses
        avg_operation_interval_ms=3600000.0,  # 1 hour average
        total_operations=15,
    )


def generate_demo_equity_curve(days: int = 30) -> List[dict]:
    """
    Generate demo equity curve data.
    
    Args:
        days: Number of days
    
    Returns:
        List of equity curve points
    """
    points = []
    base_time = datetime.now() - timedelta(days=days)
    initial_equity = 100000.0
    current_equity = initial_equity
    
    # Simulate equity curve with drawdown
    peak = initial_equity
    trend = 0.0005  # Slight upward trend
    
    for i in range(days):
        # Daily change
        daily_return = random.gauss(trend, 0.02)
        current_equity = current_equity * (1 + daily_return)
        
        # Update peak
        if current_equity > peak:
            peak = current_equity
        
        # Calculate drawdown
        drawdown = (peak - current_equity) / peak if peak > 0 else Decimal("0")
        
        points.append({
            "timestamp": (base_time + timedelta(days=i)).isoformat(),
            "equity": str(current_equity),
            "drawdown": str(drawdown),
        })
    
    return points


def generate_demo_chaos_data(days: int = 30) -> List[dict]:
    """Generate demo chaos index data"""
    data = []
    base_time = datetime.now() - timedelta(days=days)
    
    # Simulate chaos index varying over time
    for i in range(days):
        # Chaos index oscillates between 0.3 and 0.7
        chaos_index = 0.5 + 0.2 * (i % 20) / 20
        
        # Classify regime
        if chaos_index < 0.3:
            regime = RegimeState.TREND.value
        elif chaos_index > 0.7:
            regime = RegimeState.CHAOTIC.value
        else:
            regime = RegimeState.NEUTRAL.value
        
        data.append({
            "timestamp": (base_time + timedelta(days=i)).isoformat(),
            "chaos_index": chaos_index,
            "regime": regime,
            "volatility": random.uniform(0.15, 0.35),
            "noise_to_signal_ratio": random.uniform(0.5, 1.5),
        })
    
    return data


def generate_demo_strategy_result() -> dict:
    """Generate demo strategy backtest result"""
    equity_curve = generate_demo_equity_curve()
    
    return {
        "strategy_id": "demo_ma_crossover",
        "strategy_name": "Demo MA Crossover Strategy",
        "start_date": equity_curve[0]["timestamp"],
        "end_date": equity_curve[-1]["timestamp"],
        "initial_capital": "100000",
        "final_capital": str(float(equity_curve[-1]["equity"])),
        "metrics": {
            "total_return": str((float(equity_curve[-1]["equity"]) - 100000) / 100000),
            "annualized_return": str(0.15),  # 15% annualized
            "sharpe_ratio": str(1.25),
            "max_drawdown": str(0.08),  # 8% max drawdown
            "win_rate": str(0.55),  # 55% win rate
            "total_trades": 25,
            "winning_trades": 14,
            "losing_trades": 11,
            "profit_factor": str(1.45),
            "avg_r_multiple": str(1.2),
        },
        "equity_curve": equity_curve,
        "trades": [],  # Empty for now
    }

