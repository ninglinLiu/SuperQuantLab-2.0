"""
Chaos Engine: Calculate chaos metrics including Lyapunov exponent
"""
from typing import List, Tuple
from decimal import Decimal
import numpy as np
from enum import Enum

from app.models.market import Candle
from app.models.strategy import RegimeState


class ChaosEngine:
    """
    Chaos Engine calculates chaos-related metrics for market analysis.
    
    Provides:
    - Lyapunov exponent (approximation)
    - Chaos index (0-1)
    - Volatility metrics
    - Noise-to-signal ratio
    - Regime classification
    """
    
    def __init__(self, embedding_dimension: int = 3, delay: int = 1):
        """
        Initialize chaos engine.
        
        Args:
            embedding_dimension: Embedding dimension for phase space reconstruction
            delay: Time delay for phase space reconstruction
        """
        self.embedding_dimension = embedding_dimension
        self.delay = delay
    
    def calculate_returns(self, prices: List[float]) -> List[float]:
        """Calculate log returns"""
        if len(prices) < 2:
            return []
        return np.diff(np.log(prices)).tolist()
    
    def approximate_lyapunov_exponent(
        self,
        returns: List[float],
        max_time: int = 10,
    ) -> float:
        """
        Approximate the largest Lyapunov exponent.
        
        This is a simplified approximation using phase space reconstruction.
        
        Args:
            returns: Time series of returns
            max_time: Maximum time step for divergence calculation
        
        Returns:
            Approximate Lyapunov exponent (can be negative or positive)
        """
        if len(returns) < self.embedding_dimension * self.delay + max_time:
            return 0.0
        
        returns_array = np.array(returns)
        
        # Phase space reconstruction
        embedded = []
        for i in range(len(returns_array) - (self.embedding_dimension - 1) * self.delay):
            point = returns_array[i:i + self.embedding_dimension * self.delay:self.delay]
            embedded.append(point)
        
        embedded = np.array(embedded)
        
        if len(embedded) < 10:
            return 0.0
        
        # Find nearest neighbors and track divergence
        divergences = []
        
        for i in range(len(embedded) - max_time):
            # Find nearest neighbor (excluding immediate neighbors)
            distances = np.linalg.norm(embedded[i+1:] - embedded[i], axis=1)
            if len(distances) == 0:
                continue
            
            nearest_idx = np.argmin(distances) + i + 1
            initial_distance = distances[nearest_idx - i - 1]
            
            if initial_distance < 1e-10:
                continue
            
            # Track divergence over time
            for t in range(1, min(max_time, len(embedded) - nearest_idx)):
                if nearest_idx + t >= len(embedded):
                    break
                
                distance_t = np.linalg.norm(embedded[nearest_idx + t] - embedded[i + t])
                if distance_t > 0 and initial_distance > 0:
                    divergence = np.log(distance_t / initial_distance) / t
                    divergences.append(divergence)
        
        if not divergences:
            return 0.0
        
        # Average divergence = approximate Lyapunov exponent
        lyap = np.mean(divergences)
        return float(lyap)
    
    def calculate_chaos_index(
        self,
        candles: List[Candle],
        window: int = 100,
    ) -> float:
        """
        Calculate chaos index (0-1).
        
        Higher values indicate more chaotic/unpredictable market.
        
        Args:
            candles: List of candles
            window: Rolling window size
        
        Returns:
            Chaos index between 0 and 1
        """
        if len(candles) < window:
            return 0.5  # Neutral
        
        # Use recent window
        recent = candles[-window:]
        prices = [float(c.close) for c in recent]
        
        # Calculate returns
        returns = self.calculate_returns(prices)
        
        if len(returns) < 10:
            return 0.5
        
        # Calculate Lyapunov exponent
        lyap = self.approximate_lyapunov_exponent(returns)
        
        # Normalize to [0, 1]
        # Positive Lyapunov = chaotic
        # Negative Lyapunov = stable/trending
        # Map: -0.5 to 0.5 -> 0 to 1
        chaos_index = (lyap + 0.5) / 1.0
        chaos_index = max(0.0, min(1.0, chaos_index))  # Clamp to [0, 1]
        
        return chaos_index
    
    def calculate_volatility(self, candles: List[Candle], window: int = 20) -> float:
        """
        Calculate rolling volatility (annualized).
        
        Args:
            candles: List of candles
            window: Rolling window size
        
        Returns:
            Annualized volatility
        """
        if len(candles) < window:
            return 0.0
        
        recent = candles[-window:]
        prices = [float(c.close) for c in recent]
        returns = self.calculate_returns(prices)
        
        if len(returns) < 2:
            return 0.0
        
        # Standard deviation of returns
        vol = np.std(returns)
        
        # Annualize (assuming hourly data)
        vol_annualized = vol * np.sqrt(24 * 365)
        
        return float(vol_annualized)
    
    def calculate_noise_to_signal_ratio(
        self,
        candles: List[Candle],
        trend_window: int = 50,
        noise_window: int = 5,
    ) -> float:
        """
        Calculate noise-to-signal ratio.
        
        Args:
            candles: List of candles
            trend_window: Window for trend calculation
            noise_window: Window for noise calculation
        
        Returns:
            Noise-to-signal ratio (higher = more noise)
        """
        if len(candles) < trend_window:
            return 0.5
        
        prices = np.array([float(c.close) for c in candles])
        
        # Calculate trend (long-term moving average slope)
        if len(prices) >= trend_window:
            ma_long = np.mean(prices[-trend_window:])
            ma_prev = np.mean(prices[-trend_window-10:-10]) if len(prices) >= trend_window + 10 else ma_long
            trend_signal = abs(ma_long - ma_prev) / ma_prev if ma_prev > 0 else 0
        else:
            trend_signal = 0
        
        # Calculate noise (short-term volatility)
        if len(prices) >= noise_window:
            recent_returns = np.diff(np.log(prices[-noise_window:]))
            noise = np.std(recent_returns) if len(recent_returns) > 0 else 0
        else:
            noise = 0
        
        # Ratio
        if trend_signal > 0:
            ratio = noise / trend_signal
        else:
            ratio = 1.0 if noise > 0 else 0.0
        
        return float(ratio)
    
    def classify_regime(
        self,
        chaos_index: float,
        volatility: float = None,
        noise_to_signal: float = None,
    ) -> RegimeState:
        """
        Classify market regime based on chaos metrics.
        
        Args:
            chaos_index: Chaos index (0-1)
            volatility: Volatility (optional)
            noise_to_signal: Noise-to-signal ratio (optional)
        
        Returns:
            RegimeState enum
        """
        # Simple classification based on chaos index
        if chaos_index < 0.3:
            return RegimeState.TREND  # Low chaos = trending
        elif chaos_index > 0.7:
            return RegimeState.CHAOTIC  # High chaos = chaotic
        else:
            return RegimeState.NEUTRAL  # Medium chaos = neutral

