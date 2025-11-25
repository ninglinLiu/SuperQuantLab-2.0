"""
Strategies module
"""
from app.strategies.base import BaseStrategy
from app.strategies.ma_crossover import MACrossoverStrategy
from app.strategies.ma_cluster_density import MAClusterDensityStrategy

__all__ = [
    "BaseStrategy",
    "MACrossoverStrategy",
    "MAClusterDensityStrategy",
]

