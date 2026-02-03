"""
EMA 均线交叉策略
当快线上穿慢线时买入，下穿时卖出
"""
import pandas as pd
import ta
from typing import Tuple
from .base import BaseStrategy
import config


class EMACrossStrategy(BaseStrategy):
    """
    EMA 均线交叉策略
    
    参数:
        fast_window: 快速EMA周期 (默认20)
        slow_window: 慢速EMA周期 (默认60)
    """
    
    def __init__(self, fast_window: int = None, slow_window: int = None):
        super().__init__("EMA交叉策略")
        
        self.fast_window = fast_window or config.EMA_FAST_WINDOW
        self.slow_window = slow_window or config.EMA_SLOW_WINDOW
        
        self.params = {
            'fast_window': self.fast_window,
            'slow_window': self.slow_window
        }
    
    def generate_signals(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        生成交易信号
        
        买入信号: 快线上穿慢线
        卖出信号: 快线下穿慢线
        """
        df = df.copy()
        
        # 计算EMA
        df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=self.fast_window)
        df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=self.slow_window)
        
        # 生成信号
        # 金叉：快线上穿慢线
        entries = (df['ema_fast'] > df['ema_slow']) & \
                  (df['ema_fast'].shift(1) <= df['ema_slow'].shift(1))
        
        # 死叉：快线下穿慢线
        exits = (df['ema_fast'] < df['ema_slow']) & \
                (df['ema_fast'].shift(1) >= df['ema_slow'].shift(1))
        
        return entries, exits


# ==================== 使用示例 ====================
if __name__ == "__main__":
    from data.fetcher import DataFetcher
    
    # 获取数据
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 500)
    
    # 创建策略
    strategy = EMACrossStrategy(fast_window=20, slow_window=60)
    print(f"策略: {strategy}")
    
    # 生成信号
    entries, exits = strategy.generate_signals(df)
    
    print(f"\n买入信号数量: {entries.sum()}")
    print(f"卖出信号数量: {exits.sum()}")
    
    # 显示信号位置
    print("\n买入信号位置:")
    print(df[entries][['timestamp', 'close']].head())