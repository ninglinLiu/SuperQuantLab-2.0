"""
Data transformations: returns calculation, normalization, etc.
"""
from typing import List
from decimal import Decimal
import numpy as np
import pandas as pd

from app.models.market import Candle


def calculate_returns(candles: List[Candle], method: str = "simple") -> List[float]:
    """
    Calculate returns from candles.
    
    Args:
        candles: List of Candle objects
        method: "simple" or "log"
    
    Returns:
        List of returns as floats
    """
    if not candles:
        return []
    
    closes = [float(c.close) for c in candles]
    
    if method == "simple":
        returns = np.diff(closes) / closes[:-1]
    elif method == "log":
        returns = np.diff(np.log(closes))
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return returns.tolist()


def normalize_prices(candles: List[Candle], method: str = "minmax") -> List[float]:
    """
    Normalize prices to [0, 1] range.
    
    Args:
        candles: List of Candle objects
        method: "minmax" or "zscore"
    
    Returns:
        List of normalized close prices
    """
    if not candles:
        return []
    
    closes = np.array([float(c.close) for c in candles])
    
    if method == "minmax":
        min_val = closes.min()
        max_val = closes.max()
        if max_val - min_val == 0:
            return [0.5] * len(closes)
        normalized = (closes - min_val) / (max_val - min_val)
    elif method == "zscore":
        mean = closes.mean()
        std = closes.std()
        if std == 0:
            return [0.0] * len(closes)
        normalized = (closes - mean) / std
        # Map to [0, 1] if needed
        normalized = (normalized - normalized.min()) / (normalized.max() - normalized.min() + 1e-10)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return normalized.tolist()


def calculate_volatility(candles: List[Candle], window: int = 20, annualized: bool = True) -> List[float]:
    """
    Calculate rolling volatility (standard deviation of returns).
    
    Args:
        candles: List of Candle objects
        window: Rolling window size
        annualized: Whether to annualize volatility
    
    Returns:
        List of volatility values
    """
    if len(candles) < window:
        return [0.0] * len(candles)
    
    returns = calculate_returns(candles, method="simple")
    df = pd.Series(returns)
    volatility = df.rolling(window=window).std().fillna(0).tolist()
    
    # Annualize (assuming hourly data, 24*365 hours per year)
    if annualized:
        volatility = [v * np.sqrt(24 * 365) for v in volatility]
    
    # Pad with zeros for first window-1 values
    return [0.0] * (window - 1) + volatility


def calculate_moving_average(candles: List[Candle], window: int) -> List[Decimal]:
    """
    Calculate simple moving average.
    
    Args:
        candles: List of Candle objects
        window: Window size
    
    Returns:
        List of MA values as Decimals
    """
    if len(candles) < window:
        return [Decimal("0")] * len(candles)
    
    closes = [float(c.close) for c in candles]
    df = pd.Series(closes)
    ma_values = df.rolling(window=window).mean().fillna(0).tolist()
    
    return [Decimal(str(v)) for v in ma_values]

