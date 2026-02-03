"""
MACD 策略
基于MACD指标的交易策略
"""
import pandas as pd
import ta
from typing import Tuple
from .base import BaseStrategy
import config


class MACDStrategy(BaseStrategy):
    """
    MACD 策略
    
    信号逻辑:
    - 买入: MACD线上穿信号线，且MACD柱状图为正
    - 卖出: MACD线下穿信号线，且MACD柱状图为负
    
    参数:
        fast: 快速EMA周期 (默认12)
        slow: 慢速EMA周期 (默认26)
        signal: 信号线周期 (默认9)
    """
    
    def __init__(
        self,
        fast: int = None,
        slow: int = None,
        signal: int = None
    ):
        super().__init__("MACD策略")
        
        self.fast = fast or config.MACD_FAST
        self.slow = slow or config.MACD_SLOW
        self.signal = signal or config.MACD_SIGNAL
        
        self.params = {
            'fast': self.fast,
            'slow': self.slow,
            'signal': self.signal
        }
    
    def generate_signals(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        生成交易信号
        
        买入信号: MACD上穿信号线
        卖出信号: MACD下穿信号线
        """
        df = df.copy()
        
        # 计算MACD
        macd_indicator = ta.trend.MACD(
            df['close'],
            window_slow=self.slow,
            window_fast=self.fast,
            window_sign=self.signal
        )
        
        df['macd'] = macd_indicator.macd()
        df['macd_signal'] = macd_indicator.macd_signal()
        df['macd_diff'] = macd_indicator.macd_diff()
        
        # 买入信号：MACD上穿信号线（金叉）
        entries = (df['macd'] > df['macd_signal']) & \
                  (df['macd'].shift(1) <= df['macd_signal'].shift(1))
        
        # 卖出信号：MACD下穿信号线（死叉）
        exits = (df['macd'] < df['macd_signal']) & \
                (df['macd'].shift(1) >= df['macd_signal'].shift(1))
        
        return entries, exits


class MACDAdvancedStrategy(BaseStrategy):
    """
    MACD 高级策略
    
    结合MACD柱状图和零轴判断
    - 只在MACD > 0时做多
    - 只在MACD < 0时观望或做空
    """
    
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        super().__init__("MACD高级策略")
        
        self.fast = fast
        self.slow = slow
        self.signal = signal
        
        self.params = {
            'fast': self.fast,
            'slow': self.slow,
            'signal': self.signal
        }
    
    def generate_signals(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        生成交易信号（更严格的条件）
        """
        df = df.copy()
        
        # 计算MACD
        macd_indicator = ta.trend.MACD(
            df['close'],
            window_slow=self.slow,
            window_fast=self.fast,
            window_sign=self.signal
        )
        
        df['macd'] = macd_indicator.macd()
        df['macd_signal'] = macd_indicator.macd_signal()
        df['macd_diff'] = macd_indicator.macd_diff()
        
        # 买入信号：MACD金叉 且 MACD > 0（多头市场）
        entries = (df['macd'] > df['macd_signal']) & \
                  (df['macd'].shift(1) <= df['macd_signal'].shift(1)) & \
                  (df['macd'] > 0)
        
        # 卖出信号：MACD死叉 或 MACD跌破0轴
        exits = ((df['macd'] < df['macd_signal']) & \
                 (df['macd'].shift(1) >= df['macd_signal'].shift(1))) | \
                ((df['macd'] < 0) & (df['macd'].shift(1) >= 0))
        
        return entries, exits


# ==================== 使用示例 ====================
if __name__ == "__main__":
    from data.fetcher import DataFetcher
    
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "4h", 500)
    
    # 基础MACD策略
    strategy1 = MACDStrategy()
    print(f"策略1: {strategy1}")
    entries1, exits1 = strategy1.generate_signals(df)
    print(f"买入信号: {entries1.sum()}, 卖出信号: {exits1.sum()}")
    
    # 高级MACD策略
    strategy2 = MACDAdvancedStrategy()
    print(f"\n策略2: {strategy2}")
    entries2, exits2 = strategy2.generate_signals(df)
    print(f"买入信号: {entries2.sum()}, 卖出信号: {exits2.sum()}")