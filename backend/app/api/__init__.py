"""
API routes module
"""
from app.api.routes_backtest import router as backtest_router
from app.api.routes_strategies import router as strategies_router
from app.api.routes_metrics import router as metrics_router

__all__ = [
    "backtest_router",
    "strategies_router",
    "metrics_router",
]

