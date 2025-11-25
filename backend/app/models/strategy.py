"""
Strategy models: StrategyConfig, StrategyResult, RegimeState
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RegimeState(str, Enum):
    """Market regime state"""
    TREND = "TREND"
    NEUTRAL = "NEUTRAL"
    CHAOTIC = "CHAOTIC"


class StrategyType(str, Enum):
    """Strategy type"""
    MA_CROSSOVER = "ma_crossover"
    MA_CLUSTER_DENSITY = "ma_cluster_density"
    CUSTOM = "custom"


class StrategyConfig(BaseModel):
    """Strategy configuration"""
    strategy_id: str
    strategy_type: StrategyType
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v),
        }


class PerformanceMetrics(BaseModel):
    """Performance metrics"""
    total_return: Decimal = Field(default=Decimal("0"))
    annualized_return: Decimal = Field(default=Decimal("0"))
    sharpe_ratio: Decimal = Field(default=Decimal("0"))
    sortino_ratio: Optional[Decimal] = None
    max_drawdown: Decimal = Field(default=Decimal("0"))
    max_drawdown_duration: int = Field(default=0)  # in bars
    win_rate: Decimal = Field(default=Decimal("0"))
    profit_factor: Decimal = Field(default=Decimal("0"))
    avg_r_multiple: Decimal = Field(default=Decimal("0"))
    total_trades: int = Field(default=0)
    winning_trades: int = Field(default=0)
    losing_trades: int = Field(default=0)
    avg_win: Decimal = Field(default=Decimal("0"))
    avg_loss: Decimal = Field(default=Decimal("0"))

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v),
        }


class EquityPoint(BaseModel):
    """Equity curve point"""
    timestamp: datetime
    equity: Decimal
    drawdown: Decimal

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v),
        }


class StrategyResult(BaseModel):
    """Strategy backtest result"""
    strategy_id: str
    strategy_name: str
    start_date: datetime
    end_date: datetime
    initial_capital: Decimal
    final_capital: Decimal
    metrics: PerformanceMetrics
    equity_curve: List[EquityPoint] = Field(default_factory=list)
    trades: List = Field(default_factory=list)  # List of Trade objects
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v),
        }


class RegimeInfo(BaseModel):
    """Market regime information"""
    timestamp: datetime
    regime: RegimeState
    chaos_index: float = Field(ge=0, le=1)
    whale_activity_index: float = Field(ge=0, le=1)
    leverage_risk_index: float = Field(ge=0, le=1)
    position_multiplier: float = Field(ge=0, le=1)
    allow_new_trades: bool = True

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

