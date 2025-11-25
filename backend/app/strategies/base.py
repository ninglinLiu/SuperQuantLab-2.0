"""
Base strategy abstract class
"""
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from app.models.market import Bar, Signal
from app.models.strategy import StrategyConfig, StrategyResult


class BaseStrategy(ABC):
    """
    Base strategy abstract class.
    
    All strategies must implement:
    - reset(): Initialize/reset strategy state
    - on_bar(bar): Process new bar and generate signals
    - on_finish(): Return strategy result
    """
    
    def __init__(self, config: StrategyConfig):
        """
        Initialize strategy with configuration.
        
        Args:
            config: Strategy configuration
        """
        self.config = config
        self.strategy_id = config.strategy_id
        self.name = config.name
        self.params = config.parameters
        self.reset()
    
    @abstractmethod
    def reset(self) -> None:
        """
        Reset strategy state (called at start of backtest).
        """
        pass
    
    @abstractmethod
    def on_bar(self, bar: Bar) -> Optional[Signal]:
        """
        Process new bar and generate trading signal if any.
        
        Args:
            bar: Current bar/candle
        
        Returns:
            Signal object if trading action should be taken, None otherwise
        """
        pass
    
    @abstractmethod
    def on_finish(self) -> StrategyResult:
        """
        Called when backtest is finished.
        
        Returns:
            StrategyResult object with backtest results
        """
        pass
    
    def get_position_size(
        self,
        equity: float,
        risk_per_trade: float = 0.02,
        price: float = None,
        stop_loss: float = None,
    ) -> float:
        """
        Calculate position size based on risk management.
        
        Args:
            equity: Current equity
            risk_per_trade: Risk per trade as fraction (default 2%)
            price: Entry price
            stop_loss: Stop loss price
        
        Returns:
            Position size (quantity)
        """
        if price is None or stop_loss is None:
            # Use fixed percentage of equity
            return equity * risk_per_trade
        else:
            # Calculate based on stop loss distance
            risk_amount = equity * risk_per_trade
            risk_per_unit = abs(price - stop_loss)
            if risk_per_unit == 0:
                return 0
            return risk_amount / risk_per_unit

