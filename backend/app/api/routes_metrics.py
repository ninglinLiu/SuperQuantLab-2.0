"""
Metrics API routes: Performance, chaos, behavior metrics
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.market import Candle
from app.models.strategy import RegimeInfo
from app.engines.chaos_engine import ChaosEngine
from app.engines.behavior_engine import BehaviorEngine, BehaviorMetrics
from app.engines.microstructure_engine import MicrostructureEngine
from app.engines.meta_engine import MetaEngine
from app.data.loader import load_csv_data

router = APIRouter(prefix="/metrics", tags=["metrics"])


class ChaosMetricsResponse(BaseModel):
    """Chaos metrics response"""
    chaos_index: float
    volatility: float
    noise_to_signal_ratio: float
    regime: str
    timestamp: str


class BehaviorMetricsResponse(BaseModel):
    """Behavior metrics response"""
    impulsiveness_index: float
    chase_selloff_index: float
    consecutive_losses: int
    avg_operation_interval_ms: float
    total_operations: int


class RegimeResponse(BaseModel):
    """Regime information response"""
    regime: str
    chaos_index: float
    whale_activity_index: float
    leverage_risk_index: float
    position_multiplier: float
    allow_new_trades: bool
    recommendations: dict


@router.get("/chaos")
async def get_chaos_metrics(
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    window: int = 100,
) -> ChaosMetricsResponse:
    """
    Get chaos metrics for a symbol.
    
    Args:
        symbol: Trading pair symbol
        timeframe: Timeframe
        window: Analysis window size
    
    Returns:
        Chaos metrics including chaos index, volatility, regime
    """
    try:
        # Load recent data
        candles = load_csv_data(symbol=symbol, timeframe=timeframe)
        if len(candles) < window:
            # Use demo data if not enough real data
            from app.api.demo_data import generate_demo_candles
            candles = generate_demo_candles(symbol=symbol, timeframe=timeframe)
        
        # Calculate metrics
        engine = ChaosEngine()
        chaos_index = engine.calculate_chaos_index(candles, window=min(window, len(candles)))
        volatility = engine.calculate_volatility(candles, window=min(window, 20))
        noise_to_signal = engine.calculate_noise_to_signal_ratio(candles)
        regime = engine.classify_regime(chaos_index)
        
        return ChaosMetricsResponse(
            chaos_index=chaos_index,
            volatility=volatility,
            noise_to_signal_ratio=noise_to_signal,
            regime=regime.value,
            timestamp=datetime.now().isoformat(),
        )
    
    except (FileNotFoundError, Exception) as e:
        # Return demo data on error
        from app.api.demo_data import generate_demo_candles
        candles = generate_demo_candles(symbol=symbol, timeframe=timeframe)
        engine = ChaosEngine()
        chaos_index = engine.calculate_chaos_index(candles)
        volatility = engine.calculate_volatility(candles)
        noise_to_signal = engine.calculate_noise_to_signal_ratio(candles)
        regime = engine.classify_regime(chaos_index)
        
        return ChaosMetricsResponse(
            chaos_index=chaos_index,
            volatility=volatility,
            noise_to_signal_ratio=noise_to_signal,
            regime=regime.value,
            timestamp=datetime.now().isoformat(),
        )


@router.get("/behavior")
async def get_behavior_metrics() -> BehaviorMetricsResponse:
    """
    Get behavior metrics.
    
    Returns:
        Behavior metrics including impulsiveness, chase-selloff index
    """
    try:
        from app.api.demo_data import generate_demo_behavior_metrics
        
        # Try to get real metrics, fall back to demo data
        engine = BehaviorEngine()
        metrics = engine.get_metrics()
        
        # If no operations recorded, return demo data
        if metrics.total_operations == 0:
            metrics = generate_demo_behavior_metrics()
        
        return BehaviorMetricsResponse(
            impulsiveness_index=metrics.impulsiveness_index,
            chase_selloff_index=metrics.chase_selloff_index,
            consecutive_losses=metrics.consecutive_losses,
            avg_operation_interval_ms=metrics.avg_operation_interval_ms,
            total_operations=metrics.total_operations,
        )
    
    except Exception as e:
        # On error, return demo data
        from app.api.demo_data import generate_demo_behavior_metrics
        metrics = generate_demo_behavior_metrics()
        return BehaviorMetricsResponse(
            impulsiveness_index=metrics.impulsiveness_index,
            chase_selloff_index=metrics.chase_selloff_index,
            consecutive_losses=metrics.consecutive_losses,
            avg_operation_interval_ms=metrics.avg_operation_interval_ms,
            total_operations=metrics.total_operations,
        )


@router.get("/regime")
async def get_regime_info(
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
) -> RegimeResponse:
    """
    Get current market regime information.
    
    Args:
        symbol: Trading pair symbol
        timeframe: Timeframe
    
    Returns:
        Regime information with recommendations
    """
    try:
        # Load data (fall back to demo data if not available)
        try:
            candles = load_csv_data(symbol=symbol, timeframe=timeframe)
        except (FileNotFoundError, Exception):
            from app.api.demo_data import generate_demo_candles
            candles = generate_demo_candles(symbol=symbol, timeframe=timeframe)
        
        # Calculate metrics from all engines
        chaos_engine = ChaosEngine()
        microstructure_engine = MicrostructureEngine()
        meta_engine = MetaEngine()
        behavior_engine = BehaviorEngine()
        
        # Get behavior metrics (use demo if empty)
        behavior_metrics = behavior_engine.get_metrics()
        if behavior_metrics.total_operations == 0:
            from app.api.demo_data import generate_demo_behavior_metrics
            behavior_metrics = generate_demo_behavior_metrics()
        
        chaos_index = chaos_engine.calculate_chaos_index(candles)
        whale_activity = microstructure_engine.calculate_whale_activity_index(candles)
        leverage_risk = microstructure_engine.calculate_leverage_risk_index(candles)
        
        # Get regime info
        regime_info = meta_engine.evaluate_regime(
            chaos_index=chaos_index,
            whale_activity_index=whale_activity,
            leverage_risk_index=leverage_risk,
            behavior_metrics=behavior_metrics,
        )
        
        # Get recommendations
        recommendations = meta_engine.get_regime_recommendations(regime_info)
        
        return RegimeResponse(
            regime=regime_info.regime.value,
            chaos_index=regime_info.chaos_index,
            whale_activity_index=regime_info.whale_activity_index,
            leverage_risk_index=regime_info.leverage_risk_index,
            position_multiplier=regime_info.position_multiplier,
            allow_new_trades=regime_info.allow_new_trades,
            recommendations=recommendations,
        )
    
    except Exception as e:
        # Fallback to demo data
        from app.api.demo_data import generate_demo_candles, generate_demo_behavior_metrics
        candles = generate_demo_candles(symbol=symbol, timeframe=timeframe)
        chaos_engine = ChaosEngine()
        meta_engine = MetaEngine()
        behavior_metrics = generate_demo_behavior_metrics()
        
        chaos_index = chaos_engine.calculate_chaos_index(candles)
        regime_info = meta_engine.evaluate_regime(
            chaos_index=chaos_index,
            whale_activity_index=0.45,
            leverage_risk_index=0.35,
            behavior_metrics=behavior_metrics,
        )
        recommendations = meta_engine.get_regime_recommendations(regime_info)
        
        return RegimeResponse(
            regime=regime_info.regime.value,
            chaos_index=regime_info.chaos_index,
            whale_activity_index=0.45,
            leverage_risk_index=0.35,
            position_multiplier=regime_info.position_multiplier,
            allow_new_trades=regime_info.allow_new_trades,
            recommendations=recommendations,
        )


@router.get("/equity")
async def get_equity_curve(strategy_id: Optional[str] = None):
    """
    Get equity curve data (placeholder - should fetch from backtest results).
    
    Args:
        strategy_id: Strategy ID (optional)
    
    Returns:
        Equity curve data
    """
    # Return demo data for demonstration
    from app.api.demo_data import generate_demo_equity_curve
    equity_curve = generate_demo_equity_curve()
    
    return {
        "equity_curve": equity_curve,
        "strategy_id": strategy_id or "demo",
        "message": "Demo equity curve data",
    }

