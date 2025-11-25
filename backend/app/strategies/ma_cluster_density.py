"""
MA Cluster Density Strategy

Strategy that opens positions when multiple MAs cluster together (dense packing)
and exits when they diverge or break out.
"""
from typing import Optional, List, Tuple
from decimal import Decimal

from app.models.market import Bar, Signal, Side
from app.models.strategy import StrategyConfig, StrategyResult, PerformanceMetrics
from app.strategies.base import BaseStrategy
from app.data.transforms import calculate_moving_average


class MAClusterDensityStrategy(BaseStrategy):
    """
    MA Cluster Density Strategy.
    
    Opens positions when multiple MAs cluster together (within a threshold),
    then exits on breakout or divergence.
    
    Parameters:
        - ma_periods: List of MA periods (default: [5, 10, 20, 30, 50])
        - density_threshold: Max spread between MAs as percentage (default: 0.02 = 2%)
        - breakout_multiplier: Multiplier for breakout detection (default: 1.5)
        - position_size_pct: Position size as percentage of equity (default: 0.1)
    """
    
    def __init__(self, config: StrategyConfig):
        super().__init__(config)
        self.ma_periods = self.params.get("ma_periods", [5, 10, 20, 30, 50])
        self.density_threshold = self.params.get("density_threshold", 0.02)
        self.breakout_multiplier = self.params.get("breakout_multiplier", 1.5)
        self.position_size_pct = self.params.get("position_size_pct", 0.1)
        
        # Internal state
        self.bars: list[Bar] = []
        self.signals: list[Signal] = []
        self.current_position: Optional[Side] = None
        self.cluster_formed = False
    
    def reset(self) -> None:
        """Reset strategy state"""
        self.bars = []
        self.signals = []
        self.current_position = None
        self.cluster_formed = False
    
    def _calculate_ma_values(self) -> List[Decimal]:
        """Calculate current MA values for all periods"""
        ma_values = []
        for period in self.ma_periods:
            ma_list = calculate_moving_average(self.bars, period)
            if len(ma_list) > 0:
                ma_values.append(ma_list[-1])
            else:
                ma_values.append(Decimal("0"))
        return ma_values
    
    def _check_cluster_density(self, ma_values: List[Decimal], current_price: Decimal) -> Tuple[bool, Optional[Side]]:
        """
        Check if MAs form a dense cluster.
        
        Returns:
            (is_clustered, suggested_side)
        """
        if len(ma_values) < 2:
            return False, None
        
        # Filter out zero values
        valid_mas = [ma for ma in ma_values if ma > 0]
        if len(valid_mas) < 2:
            return False, None
        
        # Calculate spread (max - min) as percentage of average
        ma_avg = sum(valid_mas) / len(valid_mas)
        ma_min = min(valid_mas)
        ma_max = max(valid_mas)
        
        if ma_avg == 0:
            return False, None
        
        spread_pct = float((ma_max - ma_min) / ma_avg)
        
        # Check if clustered
        is_clustered = spread_pct <= self.density_threshold
        
        if not is_clustered:
            return False, None
        
        # Determine side based on price relative to cluster
        if current_price > ma_max * Decimal(str(1 + self.breakout_multiplier * self.density_threshold)):
            return True, Side.BUY  # Breakout above
        elif current_price < ma_min * Decimal(str(1 - self.breakout_multiplier * self.density_threshold)):
            return True, Side.SELL  # Breakout below
        else:
            # Price within cluster - wait for confirmation
            return True, None
    
    def _check_divergence(self, ma_values: List[Decimal]) -> bool:
        """
        Check if MAs have diverged (exit signal).
        
        Returns:
            True if diverged
        """
        valid_mas = [ma for ma in ma_values if ma > 0]
        if len(valid_mas) < 2:
            return False
        
        ma_avg = sum(valid_mas) / len(valid_mas)
        ma_min = min(valid_mas)
        ma_max = max(valid_mas)
        
        if ma_avg == 0:
            return False
        
        spread_pct = float((ma_max - ma_min) / ma_avg)
        
        # Diverged if spread exceeds threshold * breakout_multiplier
        return spread_pct > self.density_threshold * self.breakout_multiplier
    
    def on_bar(self, bar: Bar) -> Optional[Signal]:
        """
        Process bar and generate signal based on MA cluster density.
        
        Args:
            bar: Current bar
        
        Returns:
            Signal if action should be taken, None otherwise
        """
        self.bars.append(bar)
        
        # Need enough bars for longest MA
        max_period = max(self.ma_periods)
        if len(self.bars) < max_period:
            return None
        
        # Calculate MA values
        ma_values = self._calculate_ma_values()
        
        # Check for cluster and signals
        is_clustered, suggested_side = self._check_cluster_density(ma_values, bar.close)
        
        signal = None
        
        # Entry logic: cluster formed and breakout
        if is_clustered and suggested_side and not self.cluster_formed:
            self.cluster_formed = True
            
            # Close opposite position if exists
            if self.current_position and self.current_position != suggested_side:
                close_side = Side.SELL if self.current_position == Side.BUY else Side.BUY
                signal = Signal(
                    timestamp=bar.timestamp,
                    symbol=bar.symbol,
                    side=close_side,
                    price=bar.close,
                    reason="MA cluster: close opposite position",
                )
                self.signals.append(signal)
                self.current_position = None
            
            # Open new position
            if not self.current_position:
                signal = Signal(
                    timestamp=bar.timestamp,
                    symbol=bar.symbol,
                    side=suggested_side,
                    price=bar.close,
                    quantity=Decimal(str(self.position_size_pct)),
                    reason=f"MA cluster density breakout: {suggested_side.value}",
                )
                self.current_position = suggested_side
        
        # Exit logic: divergence detected
        elif self.cluster_formed and self._check_divergence(ma_values):
            if self.current_position:
                close_side = Side.SELL if self.current_position == Side.BUY else Side.BUY
                signal = Signal(
                    timestamp=bar.timestamp,
                    symbol=bar.symbol,
                    side=close_side,
                    price=bar.close,
                    reason="MA cluster divergence: exit position",
                )
                self.current_position = None
                self.cluster_formed = False
        
        # Reset cluster flag if not clustered anymore
        if not is_clustered:
            self.cluster_formed = False
        
        if signal:
            self.signals.append(signal)
        
        return signal
    
    def on_finish(self) -> StrategyResult:
        """Generate strategy result (placeholder)"""
        from datetime import datetime
        
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

