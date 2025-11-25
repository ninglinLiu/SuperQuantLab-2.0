"""
Microstructure Engine: Analyze market microstructure (whale activity, leverage risk)
"""
from typing import List, Dict
from decimal import Decimal
import numpy as np

from app.models.market import Candle, Trade


class MicrostructureEngine:
    """
    Microstructure Engine analyzes market microstructure factors.
    
    Tracks:
    - Whale activity (large volume trades)
    - Leverage risk (open interest, funding rates)
    - Liquidation density
    """
    
    def __init__(self):
        """Initialize microstructure engine"""
        self.trades: List[Trade] = []
        self.large_trades: List[Trade] = []
        self.volume_threshold_ratio = 0.01  # 1% of avg volume = large trade
    
    def record_trade(self, trade: Trade) -> None:
        """Record a trade for analysis"""
        self.trades.append(trade)
    
    def calculate_whale_activity_index(
        self,
        candles: List[Candle],
        window: int = 100,
    ) -> float:
        """
        Calculate whale activity index (0-1).
        
        Based on:
        - Large volume trades
        - Volume spikes
        - Unusual trading patterns
        
        Args:
            candles: List of candles
            window: Analysis window
        
        Returns:
            Whale activity index (0-1), higher = more whale activity
        """
        if len(candles) < window:
            return 0.0
        
        recent = candles[-window:]
        volumes = [float(c.volume) for c in recent]
        
        if not volumes:
            return 0.0
        
        avg_volume = np.mean(volumes)
        std_volume = np.std(volumes)
        
        if avg_volume == 0:
            return 0.0
        
        # Count large volume candles (above mean + 2*std)
        threshold = avg_volume + 2 * std_volume
        large_volume_count = sum(1 for v in volumes if v > threshold)
        
        # Calculate index
        activity_ratio = large_volume_count / len(volumes)
        
        # Also check for large trades
        large_trade_ratio = 0.0
        if self.trades:
            trade_volumes = [float(t.quantity * t.price) for t in self.trades[-100:]]
            if trade_volumes:
                avg_trade_volume = np.mean(trade_volumes)
                large_trades = [v for v in trade_volumes if v > avg_volume * self.volume_threshold_ratio]
                large_trade_ratio = len(large_trades) / len(trade_volumes)
        
        # Combine metrics
        whale_index = (activity_ratio * 0.6 + large_trade_ratio * 0.4)
        
        return float(min(1.0, whale_index))
    
    def calculate_leverage_risk_index(
        self,
        candles: List[Candle],
        mock_oi_data: Dict[str, float] = None,
        mock_funding_rate: float = None,
    ) -> float:
        """
        Calculate leverage risk index (0-1).
        
        Based on:
        - Open interest (OI)
        - Funding rates
        - Price volatility
        
        Args:
            candles: List of candles
            mock_oi_data: Mock OI data (timestamp -> OI value)
            mock_funding_rate: Mock funding rate
        
        Returns:
            Leverage risk index (0-1), higher = more risk
        """
        if len(candles) < 20:
            return 0.0
        
        risk_factors = []
        
        # Factor 1: Volatility (high vol = high risk)
        prices = [float(c.close) for c in candles[-50:]]
        if len(prices) >= 2:
            returns = np.diff(np.log(prices))
            volatility = np.std(returns)
            # Normalize volatility (0-1)
            vol_factor = min(1.0, volatility * 100)  # Rough normalization
            risk_factors.append(vol_factor * 0.4)
        
        # Factor 2: Open Interest (if available)
        if mock_oi_data:
            # Use mock OI to estimate leverage
            oi_values = list(mock_oi_data.values())
            if oi_values:
                oi_ratio = max(oi_values) / min(oi_values) if min(oi_values) > 0 else 1.0
                oi_factor = min(1.0, (oi_ratio - 1.0) / 2.0)  # Normalize
                risk_factors.append(oi_factor * 0.3)
        else:
            # Placeholder: use volume as proxy
            volumes = [float(c.volume) for c in candles[-50:]]
            if volumes:
                volume_volatility = np.std(volumes) / np.mean(volumes) if np.mean(volumes) > 0 else 0
                risk_factors.append(min(1.0, volume_volatility) * 0.3)
        
        # Factor 3: Funding rate (if available)
        if mock_funding_rate is not None:
            # High absolute funding rate = high leverage risk
            funding_factor = min(1.0, abs(mock_funding_rate) * 100)  # Normalize
            risk_factors.append(funding_factor * 0.3)
        else:
            risk_factors.append(0.1)  # Default low risk
        
        # Combine factors
        leverage_risk = sum(risk_factors) if risk_factors else 0.0
        
        return float(min(1.0, leverage_risk))
    
    def get_mock_oi_data(self, candles: List[Candle]) -> Dict[str, float]:
        """
        Generate mock OI data (placeholder).
        
        TODO: Replace with real exchange API integration
        
        Returns:
            Dict mapping timestamp strings to OI values
        """
        # Mock: simulate OI based on volume
        oi_data = {}
        for candle in candles[-100:]:
            # Mock OI = volume * random factor
            mock_oi = float(candle.volume) * np.random.uniform(0.5, 2.0)
            oi_data[candle.timestamp.isoformat()] = mock_oi
        
        return oi_data
    
    def reset(self) -> None:
        """Reset all tracking data"""
        self.trades = []
        self.large_trades = []

