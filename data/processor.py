"""
数据处理模块
负责计算技术指标、数据清洗等
"""
import pandas as pd
import numpy as np
import ta


class DataProcessor:
    """数据处理器"""
    
    @staticmethod
    def add_technical_indicators(df: pd.DataFrame, indicators: list = None) -> pd.DataFrame:
        """
        添加技术指标
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
            indicators: 要计算的指标列表，None表示计算所有常用指标
            
        Returns:
            添加了技术指标的 DataFrame
        """
        df = df.copy()
        
        if indicators is None:
            indicators = ['ema', 'sma', 'rsi', 'macd', 'bb', 'atr', 'volume']
        
        # 趋势指标
        if 'ema' in indicators:
            df['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
            df['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
            df['ema_50'] = ta.trend.ema_indicator(df['close'], window=50)
        
        if 'sma' in indicators:
            df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
            df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
            df['sma_200'] = ta.trend.sma_indicator(df['close'], window=200)
        
        # 动量指标
        if 'rsi' in indicators:
            df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        
        if 'macd' in indicators:
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()
        
        # 波动率指标
        if 'bb' in indicators:
            bb = ta.volatility.BollingerBands(df['close'])
            df['bb_high'] = bb.bollinger_hband()
            df['bb_mid'] = bb.bollinger_mavg()
            df['bb_low'] = bb.bollinger_lband()
            df['bb_width'] = (df['bb_high'] - df['bb_low']) / df['bb_mid']
        
        if 'atr' in indicators:
            df['atr'] = ta.volatility.average_true_range(
                df['high'], df['low'], df['close'], window=14
            )
        
        # 成交量指标
        if 'volume' in indicators:
            df['volume_sma'] = ta.volume.volume_weighted_average_price(
                df['high'], df['low'], df['close'], df['volume']
            )
        
        return df
    
    @staticmethod
    def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
        """计算收益率"""
        df = df.copy()
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        df['cumulative_returns'] = (1 + df['returns']).cumprod() - 1
        return df
    
    @staticmethod
    def detect_support_resistance(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        检测支撑位和阻力位
        
        Args:
            df: OHLCV数据
            window: 检测窗口
            
        Returns:
            添加支撑位和阻力位的DataFrame
        """
        df = df.copy()
        
        # 滚动窗口内的最高价和最低价
        df['resistance'] = df['high'].rolling(window=window).max()
        df['support'] = df['low'].rolling(window=window).min()
        
        return df
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        数据清洗
        - 删除重复行
        - 填充缺失值
        - 删除异常值
        """
        df = df.copy()
        
        # 删除重复的时间戳
        df = df.drop_duplicates(subset=['timestamp'], keep='first')
        
        # 按时间排序
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # 填充缺失值（向前填充）
        df = df.ffill()
        
        # 删除仍然存在的缺失值
        df = df.dropna()
        
        return df
    
    @staticmethod
    def resample_data(
        df: pd.DataFrame,
        timeframe: str,
        timestamp_col: str = 'timestamp'
    ) -> pd.DataFrame:
        """
        重采样数据到不同时间周期
        
        Args:
            df: 原始数据
            timeframe: 目标时间周期 ('1h', '4h', '1d'等)
            timestamp_col: 时间戳列名
            
        Returns:
            重采样后的数据
        """
        df = df.copy()
        df = df.set_index(timestamp_col)
        
        # 定义聚合规则
        ohlc_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        
        # 重采样
        df_resampled = df.resample(timeframe).agg(ohlc_dict)
        df_resampled = df_resampled.dropna()
        df_resampled = df_resampled.reset_index()
        
        return df_resampled


# ==================== 使用示例 ====================
if __name__ == "__main__":
    from data.fetcher import DataFetcher
    
    # 获取数据
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 500)
    
    # 处理数据
    processor = DataProcessor()
    
    # 添加技术指标
    df = processor.add_technical_indicators(df)
    print("\n添加技术指标后:")
    print(df.columns.tolist())
    print(df[['timestamp', 'close', 'rsi', 'macd', 'ema_12']].tail())
    
    # 计算收益率
    df = processor.calculate_returns(df)
    print("\n添加收益率后:")
    print(df[['timestamp', 'close', 'returns', 'cumulative_returns']].tail())