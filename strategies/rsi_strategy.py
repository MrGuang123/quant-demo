"""
RSI 策略
基于相对强弱指标的超买超卖策略
"""
import pandas as pd
import ta
from typing import Tuple
from .base import BaseStrategy
import config


class RSIStrategy(BaseStrategy):
    """
    RSI 超买超卖策略
    
    参数:
        period: RSI周期 (默认14)
        oversold: 超卖线 (默认30)
        overbought: 超买线 (默认70)
    """
    
    def __init__(
        self,
        period: int = None,
        oversold: int = None,
        overbought: int = None
    ):
        super().__init__("RSI策略")
        
        self.period = period or config.RSI_PERIOD
        self.oversold = oversold or config.RSI_OVERSOLD
        self.overbought = overbought or config.RSI_OVERBOUGHT
        
        self.params = {
            'period': self.period,
            'oversold': self.oversold,
            'overbought': self.overbought
        }
    
    def generate_signals(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        生成交易信号
        
        买入信号: RSI从超卖区向上突破
        卖出信号: RSI从超买区向下突破
        """
        df = df.copy()
        
        # 计算RSI
        df['rsi'] = ta.momentum.rsi(df['close'], window=self.period)
        
        # 买入信号：RSI从下方突破超卖线
        entries = (df['rsi'] > self.oversold) & \
                  (df['rsi'].shift(1) <= self.oversold)
        
        # 卖出信号：RSI从上方跌破超买线
        exits = (df['rsi'] < self.overbought) & \
                (df['rsi'].shift(1) >= self.overbought)
        
        return entries, exits


# ==================== 使用示例 ====================
if __name__ == "__main__":
    from data.fetcher import DataFetcher
    
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 500)
    
    strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    print(f"策略: {strategy}")
    
    entries, exits = strategy.generate_signals(df)
    
    print(f"\n买入信号: {entries.sum()}")
    print(f"卖出信号: {exits.sum()}")