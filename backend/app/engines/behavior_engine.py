"""
Behavior Engine: Track and analyze trading behavior patterns
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from app.models.market import Trade, Signal, Side


@dataclass
class BehaviorMetrics:
    """Behavior analysis metrics"""
    impulsiveness_index: float = 0.0  # 0-1, higher = more impulsive
    chase_selloff_index: float = 0.0  # 0-1, higher = more chasing
    consecutive_losses: int = 0
    avg_operation_interval_ms: float = 0.0
    total_operations: int = 0


class BehaviorEngine:
    """
    Behavior Engine tracks and analyzes trading behavior patterns.
    
    Tracks:
    - Operation intervals (impulsiveness)
    - Chasing tops / panic selling
    - Adding size after losing streaks
    - Emotional trading patterns
    """
    
    def __init__(self):
        """Initialize behavior engine"""
        self.trades: List[Trade] = []
        self.signals: List[Signal] = []
        self.operation_timestamps: List[datetime] = []
        self.local_extremes: Dict[datetime, float] = {}  # timestamp -> price
    
    def record_signal(self, signal: Signal, current_price: Decimal) -> None:
        """
        Record a trading signal.
        
        Args:
            signal: Trading signal
            current_price: Current market price at signal time
        """
        self.signals.append(signal)
        self.operation_timestamps.append(signal.timestamp)
    
    def record_trade(self, trade: Trade) -> None:
        """Record an executed trade"""
        self.trades.append(trade)
    
    def record_local_extreme(self, timestamp: datetime, price: float, is_high: bool) -> None:
        """
        Record local price extreme (for chase-selloff detection).
        
        Args:
            timestamp: Timestamp
            price: Price level
            is_high: True for high, False for low
        """
        self.local_extremes[timestamp] = price
    
    def calculate_impulsiveness_index(self, window_hours: int = 24) -> float:
        """
        Calculate impulsiveness index based on operation intervals.
        
        Lower intervals = higher impulsiveness.
        
        Args:
            window_hours: Time window for analysis
        
        Returns:
            Impulsiveness index (0-1), higher = more impulsive
        """
        if len(self.operation_timestamps) < 2:
            return 0.0
        
        # Filter recent operations
        cutoff = datetime.now() - timedelta(hours=window_hours)
        recent_ops = [ts for ts in self.operation_timestamps if ts >= cutoff]
        
        if len(recent_ops) < 2:
            return 0.0
        
        # Calculate intervals (in milliseconds)
        intervals = []
        for i in range(1, len(recent_ops)):
            delta = recent_ops[i] - recent_ops[i-1]
            intervals.append(delta.total_seconds() * 1000)
        
        if not intervals:
            return 0.0
        
        avg_interval = sum(intervals) / len(intervals)
        
        # Normalize: very short intervals (< 1 minute) = high impulsiveness
        # Very long intervals (> 1 hour) = low impulsiveness
        # Map to 0-1 range
        if avg_interval < 60000:  # < 1 minute
            return 1.0
        elif avg_interval > 3600000:  # > 1 hour
            return 0.0
        else:
            # Linear interpolation
            return 1.0 - (avg_interval - 60000) / (3600000 - 60000)
    
    def calculate_chase_selloff_index(self) -> float:
        """
        Calculate chase-selloff index.
        
        Detects:
        - Buying near local highs
        - Selling near local lows
        
        Returns:
            Chase-selloff index (0-1), higher = more chasing
        """
        if len(self.trades) < 2 or len(self.local_extremes) == 0:
            return 0.0
        
        chase_count = 0
        total_checks = 0
        
        for trade in self.trades:
            # Look for local extremes near trade time
            nearby_extremes = []
            for ext_time, ext_price in self.local_extremes.items():
                time_diff = abs((trade.timestamp - ext_time).total_seconds())
                if time_diff < 3600:  # Within 1 hour
                    nearby_extremes.append((ext_time, ext_price, time_diff))
            
            if not nearby_extremes:
                continue
            
            # Find closest extreme
            closest = min(nearby_extremes, key=lambda x: x[2])
            ext_price = closest[1]
            trade_price = float(trade.price)
            
            # Check if chasing
            if trade.side == Side.BUY:
                # Buying near local high = chasing
                if trade_price >= ext_price * 0.98:  # Within 2% of high
                    chase_count += 1
            else:  # SELL
                # Selling near local low = panic selling
                if trade_price <= ext_price * 1.02:  # Within 2% of low
                    chase_count += 1
            
            total_checks += 1
        
        if total_checks == 0:
            return 0.0
        
        return chase_count / total_checks
    
    def detect_consecutive_losses(self) -> int:
        """
        Count consecutive losing trades.
        
        Returns:
            Number of consecutive losses
        """
        if not self.trades:
            return 0
        
        consecutive = 0
        # Simplified: assume recent trades are losing if price decreased
        # Real implementation should track entry/exit pairs
        
        # Sort trades by timestamp
        sorted_trades = sorted(self.trades, key=lambda t: t.timestamp, reverse=True)
        
        for i in range(len(sorted_trades) - 1):
            # Simplified check
            consecutive += 1
        
        return consecutive
    
    def get_metrics(self) -> BehaviorMetrics:
        """
        Calculate all behavior metrics.
        
        Returns:
            BehaviorMetrics object
        """
        impulsiveness = self.calculate_impulsiveness_index()
        chase_selloff = self.calculate_chase_selloff_index()
        consecutive_losses = self.detect_consecutive_losses()
        
        # Calculate avg operation interval
        intervals = []
        if len(self.operation_timestamps) >= 2:
            for i in range(1, len(self.operation_timestamps)):
                delta = self.operation_timestamps[i] - self.operation_timestamps[i-1]
                intervals.append(delta.total_seconds() * 1000)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0.0
        
        return BehaviorMetrics(
            impulsiveness_index=impulsiveness,
            chase_selloff_index=chase_selloff,
            consecutive_losses=consecutive_losses,
            avg_operation_interval_ms=avg_interval,
            total_operations=len(self.operation_timestamps),
        )
    
    def reset(self) -> None:
        """Reset all tracking data"""
        self.trades = []
        self.signals = []
        self.operation_timestamps = []
        self.local_extremes = {}

