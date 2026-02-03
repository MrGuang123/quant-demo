"""
数据获取模块
负责从交易所获取历史K线数据
"""
import ccxt
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Optional, List
import config


class DataFetcher:
    """数据获取器"""

    # 交易所配置映射
    EXCHANGE_CONFIGS = {
        'binance': {
            'symbol_format': 'slash',  # BTC/USDT
            'quote_currency': 'USDT'
        },
        'okx': {
            'symbol_format': 'slash',  # BTC/USDT
            'quote_currency': 'USDT'
        },
        'bybit': {
            'symbol_format': 'slash',  # BTC/USDT
            'quote_currency': 'USDT'
        },
        'coinbase': {
            'symbol_format': 'dash',   # BTC-USD
            'quote_currency': 'USD'
        }
    }
    
    def __init__(self, exchange_name: str = config.DEFAULT_EXCHANGE):
        """
        初始化数据获取器
        
        Args:
            exchange_name: 交易所名称 (binance, okx, bybit等)
        """
        self.exchange_name = exchange_name
        self.exchange = self._init_exchange(exchange_name)
        self.cache_dir = config.DATA_DIR / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
    def _init_exchange(self, exchange_name: str):
        """初始化交易所连接"""
        exchange_class = getattr(ccxt, exchange_name)
        
        # 如果有API密钥，可以进行认证
        if config.BINANCE_API_KEY and exchange_name == "binance":
            return exchange_class({
                'apiKey': config.BINANCE_API_KEY,
                'secret': config.BINANCE_API_SECRET,
                'enableRateLimit': True,  # 启用限速
            })
        else:
            return exchange_class({'enableRateLimit': True})
    
    def normalize_symbol(self, symbol: str) -> str:
        """
        自动转换交易对格式以适配不同交易所
        
        输入统一格式：BTC/USDT
        输出根据交易所自动转换：
        - Binance/OKX/Bybit: BTC/USDT
        - Coinbase: BTC-USD
        
        Args:
            symbol: 统一格式的交易对，如 'BTC/USDT'
            
        Returns:
            适配交易所的交易对格式
        """
        # 获取交易所配置
        exchange_config = self.EXCHANGE_CONFIGS.get(
            self.exchange_name,
            {'symbol_format': 'slash', 'quote_currency': 'USDT'}
        )
        
        # 解析输入的交易对
        if '/' in symbol:
            base, quote = symbol.split('/')
        elif '-' in symbol:
            base, quote = symbol.split('-')
        else:
            return symbol  # 无法解析，返回原值
        
        # 根据交易所要求的计价货币转换
        target_quote = exchange_config['quote_currency']
        if quote in ['USDT', 'USD', 'BUSD', 'USDC']:
            quote = target_quote
        
        # 根据交易所格式要求转换
        if exchange_config['symbol_format'] == 'dash':
            return f"{base}-{quote}"
        else:
            return f"{base}/{quote}"
    
    def fetch_ohlcv(
        self,
        symbol: str = config.DEFAULT_SYMBOL,
        timeframe: str = config.DEFAULT_TIMEFRAME,
        limit: int = config.DATA_LIMIT,
        use_cache: bool = config.CACHE_ENABLED
    ) -> pd.DataFrame:
        """
        获取OHLCV数据（自动适配交易所格式）
        
        Args:
            symbol: 统一格式交易对，如 'BTC/USDT'（会自动转换）
            timeframe: 时间周期
            limit: K线数量
            use_cache: 是否使用缓存
        """
        # 🔥 关键：自动转换交易对格式
        normalized_symbol = self.normalize_symbol(symbol)
        
        print(f"🌐 从 {self.exchange_name} 获取 {normalized_symbol} {timeframe} 数据...")
        
        # 检查缓存（使用原始symbol作为缓存key）
        cache_file = self._get_cache_filename(symbol, timeframe, limit)
        if use_cache and cache_file.exists():
            print(f"📦 从缓存加载数据: {cache_file.name}")
            return pd.read_csv(cache_file, parse_dates=['timestamp'])
        
        try:
            # 使用转换后的交易对格式获取数据
            bars = self.exchange.fetch_ohlcv(
                normalized_symbol, 
                timeframe=timeframe, 
                limit=limit
            )
            
            df = pd.DataFrame(
                bars,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # 保存到缓存
            if use_cache:
                df.to_csv(cache_file, index=False)
                print(f"💾 数据已缓存到: {cache_file.name}")
            
            print(f"✅ 获取成功: {len(df)} 根K线")
            return df
            
        except Exception as e:
            print(f"❌ 获取数据失败: {e}")
            raise
    
    def fetch_multiple_symbols(
        self,
        symbols: List[str],
        timeframe: str = config.DEFAULT_TIMEFRAME,
        limit: int = config.DATA_LIMIT
    ) -> dict:
        """
        获取多个交易对的数据
        
        Args:
            symbols: 交易对列表
            timeframe: 时间周期
            limit: K线数量
            
        Returns:
            字典 {symbol: DataFrame}
        """
        data = {}
        for symbol in symbols:
            print(f"\n处理 {symbol}...")
            try:
                df = self.fetch_ohlcv(symbol, timeframe, limit)
                data[symbol] = df
            except Exception as e:
                print(f"⚠️  {symbol} 获取失败: {e}")
                continue
        
        return data
    
    def get_exchange_info(self, symbol: str) -> dict:
        """
        获取交易对信息
        
        Returns:
            包含交易对详细信息的字典
        """
        try:
            markets = self.exchange.load_markets()
            if symbol in markets:
                return markets[symbol]
            else:
                print(f"❌ 交易对 {symbol} 不存在")
                return {}
        except Exception as e:
            print(f"❌ 获取交易对信息失败: {e}")
            return {}
    
    def _get_cache_filename(self, symbol: str, timeframe: str, limit: int) -> Path:
        """生成缓存文件名"""
        safe_symbol = symbol.replace('/', '_')
        filename = f"{self.exchange_name}_{safe_symbol}_{timeframe}_{limit}.csv"
        return self.cache_dir / filename
    
    def clear_cache(self):
        """清空所有缓存"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir()
            print("🗑️  缓存已清空")


# ==================== 使用示例 ====================
if __name__ == "__main__":
    # 创建数据获取器
    fetcher = DataFetcher("binance")
    
    # 获取单个交易对数据
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 500)
    print("\n数据预览:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"时间范围: {df['timestamp'].min()} 到 {df['timestamp'].max()}")
    
    # 获取多个交易对
    # symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    # data = fetcher.fetch_multiple_symbols(symbols, "1h", 100)