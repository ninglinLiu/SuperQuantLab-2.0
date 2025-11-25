"""
Backtest API routes
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from app.models.strategy import StrategyConfig, StrategyResult
from app.models.market import Candle
from app.engines.backtest_engine import BacktestEngine
from app.data.loader import load_csv_data

router = APIRouter(prefix="/backtest", tags=["backtest"])


class BacktestRequest(BaseModel):
    """Backtest request model"""
    strategy_configs: List[dict]  # List of StrategyConfig dicts
    symbol: str = "BTCUSDT"
    timeframe: str = "1h"
    start_date: Optional[str] = None  # ISO format
    end_date: Optional[str] = None  # ISO format
    initial_capital: float = 100000.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005


class BacktestResponse(BaseModel):
    """Backtest response model"""
    result: dict  # StrategyResult dict
    success: bool = True
    message: Optional[str] = None


@router.post("/run", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """
    Run backtest on historical data.
    
    Args:
        request: Backtest request parameters
    
    Returns:
        Backtest result with metrics and equity curve
    """
    try:
        # Parse dates
        start_date = None
        end_date = None
        if request.start_date:
            start_date = datetime.fromisoformat(request.start_date.replace("Z", "+00:00"))
        if request.end_date:
            end_date = datetime.fromisoformat(request.end_date.replace("Z", "+00:00"))
        
        # Load data (use demo data if file not found)
        try:
            candles_data = load_csv_data(
                symbol=request.symbol,
                timeframe=request.timeframe,
                start=start_date,
                end=end_date,
            )
        except FileNotFoundError:
            # Use demo data if file not found
            from app.api.demo_data import generate_demo_candles
            candles_data = generate_demo_candles(
                symbol=request.symbol,
                timeframe=request.timeframe,
                days=30,
            )
        
        # Convert to Candle objects (already done by load_csv_data)
        candles = candles_data
        
        # Parse strategy configs
        strategy_configs = []
        for config_dict in request.strategy_configs:
            config = StrategyConfig(**config_dict)
            strategy_configs.append(config)
        
        # Create backtest engine
        engine = BacktestEngine(
            initial_capital=Decimal(str(request.initial_capital)),
            fee_rate=Decimal(str(request.fee_rate)),
            slippage_rate=Decimal(str(request.slippage_rate)),
        )
        
        # Run backtest
        result = engine.run(strategy_configs, candles)
        
        # Convert result to dict
        result_dict = result.model_dump(mode="json")
        
        return BacktestResponse(
            result=result_dict,
            success=True,
            message="Backtest completed successfully",
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")

