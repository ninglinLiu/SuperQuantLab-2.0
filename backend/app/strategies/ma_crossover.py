"""
Moving Average Crossover Strategy

Simple strategy that generates signals when short MA crosses above/below long MA.
"""
from typing import Optional
from decimal import Decimal

from app.models.market import Bar, Signal, Side
from app.models.strategy import StrategyConfig, StrategyResult, PerformanceMetrics, EquityPoint
from app.strategies.base import BaseStrategy
from app.data.transforms import calculate_moving_average


class MACrossoverStrategy(BaseStrategy):
    """
    Moving Average Crossover Strategy.
    
    Parameters:
        - short_window: Short MA period (default: 10)
        - long_window: Long MA period (default: 30)
        - position_size_pct: Position size as percentage of equity (default: 0.1)
    """
    
    def __init__(self, config: StrategyConfig):
        super().__init__(config)
        self.short_window = self.params.get("short_window", 10)
        self.long_window = self.params.get("long_window", 30)
        self.position_size_pct = self.params.get("position_size_pct", 0.1)
        
        # Internal state
        self.bars: list[Bar] = []
        self.signals: list[Signal] = []
        self.current_position: Optional[Side] = None
    
    def reset(self) -> None:
        """Reset strategy state"""
        self.bars = []
        self.signals = []
        self.current_position = None
    
    def on_bar(self, bar: Bar) -> Optional[Signal]:
        """
        Process bar and generate signal if MA crossover occurs.
        
        Args:
            bar: Current bar
        
        Returns:
            Signal if crossover detected, None otherwise
        """
        self.bars.append(bar)
        
        # Need enough bars to calculate MAs
        if len(self.bars) < self.long_window:
            return None
        
        # Calculate moving averages
        short_ma_list = calculate_moving_average(self.bars, self.short_window)
        long_ma_list = calculate_moving_average(self.bars, self.long_window)
        
        if len(short_ma_list) < 2 or len(long_ma_list) < 2:
            return None
        
        short_ma_prev = short_ma_list[-2]
        short_ma_curr = short_ma_list[-1]
        long_ma_prev = long_ma_list[-2]
        long_ma_curr = long_ma_list[-1]
        
        # Check for crossover
        signal = None
        
        # Bullish crossover: short MA crosses above long MA
        if short_ma_prev <= long_ma_prev and short_ma_curr > long_ma_curr:
            if self.current_position != Side.BUY:
                # Close existing short if any, then open long
                if self.current_position == Side.SELL:
                    signal = Signal(
                        timestamp=bar.timestamp,
                        symbol=bar.symbol,
                        side=Side.BUY,  # Close short
                        price=bar.close,
                        reason="MA crossover: close short",
                    )
                    self.signals.append(signal)
                    self.current_position = None
                
                # Open long position
                signal = Signal(
                    timestamp=bar.timestamp,
                    symbol=bar.symbol,
                    side=Side.BUY,
                    price=bar.close,
                    quantity=Decimal(str(self.position_size_pct)),  # Percentage of equity
                    reason=f"MA crossover: {self.short_window}MA crosses above {self.long_window}MA",
                )
                self.current_position = Side.BUY
        
        # Bearish crossover: short MA crosses below long MA
        elif short_ma_prev >= long_ma_prev and short_ma_curr < long_ma_curr:
            if self.current_position != Side.SELL:
                # Close existing long if any, then open short
                if self.current_position == Side.BUY:
                    signal = Signal(
                        timestamp=bar.timestamp,
                        symbol=bar.symbol,
                        side=Side.SELL,  # Close long
                        price=bar.close,
                        reason="MA crossover: close long",
                    )
                    self.signals.append(signal)
                    self.current_position = None
                
                # Open short position
                signal = Signal(
                    timestamp=bar.timestamp,
                    symbol=bar.symbol,
                    side=Side.SELL,
                    price=bar.close,
                    quantity=Decimal(str(self.position_size_pct)),
                    reason=f"MA crossover: {self.short_window}MA crosses below {self.long_window}MA",
                )
                self.current_position = Side.SELL
        
        if signal:
            self.signals.append(signal)
        
        return signal
    
    def on_finish(self) -> StrategyResult:
        """
        Generate strategy result (placeholder - real calculation done in backtest engine).
        
        Returns:
            StrategyResult with basic info
        """
        from datetime import datetime
        
        # This is just a placeholder - actual metrics are calculated in backtest engine
        metrics = PerformanceMetrics()
        
        result = StrategyResult(
            strategy_id=self.strategy_id,
            strategy_name=self.name,
            start_date=self.bars[0].timestamp if self.bars else datetime.now(),
            end_date=self.bars[-1].timestamp if self.bars else datetime.now(),
            initial_capital=Decimal("100000"),
            final_capital=Decimal("100000"),
            metrics=metrics,
            equity_curve=[],
            trades=[],
        )
        
        return result

