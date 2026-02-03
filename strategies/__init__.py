"""
策略模块
"""
from .base import BaseStrategy
from .ema_cross import EMACrossStrategy
from .rsi_strategy import RSIStrategy
from .macd_strategy import MACDStrategy

__all__ = [
    "BaseStrategy",
    "EMACrossStrategy",
    "RSIStrategy",
    "MACDStrategy"
]