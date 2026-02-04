"""
全局配置文件
"""
import os
from pathlib import Path

# ==================== 项目路径 ====================
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
LOGS_DIR = PROJECT_ROOT / "logs"

# 确保目录存在
for dir_path in [DATA_DIR, RESULTS_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# ==================== 交易所配置 ====================
# DEFAULT_EXCHANGE = "binance"
DEFAULT_EXCHANGE = "coinbase"
# DEFAULT_SYMBOL = "BTC/USDT"
DEFAULT_SYMBOL = "BTC-USD"
DEFAULT_TIMEFRAME = "1h"

# 支持的交易所
SUPPORTED_EXCHANGES = ["binance", "okx", "bybit", "coinbase"]

# ==================== 回测配置 ====================
INITIAL_CAPITAL = 10000  # 初始资金（USDT）
TRADING_FEE = 0.0004     # 交易手续费 0.04%
SLIPPAGE = 0.0001        # 滑点 0.01%

# ==================== 策略配置 ====================
# EMA 交叉策略参数
EMA_FAST_WINDOW = 20
EMA_SLOW_WINDOW = 60

# RSI 策略参数
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD 策略参数
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ==================== 风险管理 ====================
MAX_POSITION_SIZE = 0.95  # 最大仓位（95%资金）
STOP_LOSS_PCT = 0.02      # 止损比例（2%）
TAKE_PROFIT_PCT = 0.04    # 止盈比例（4%）

# ==================== 数据配置 ====================
DATA_LIMIT = 1000         # 默认获取的K线数量
CACHE_ENABLED = True      # 是否启用数据缓存

# ==================== API密钥配置（不要提交到Git）====================
# 方式1：从环境变量读取
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# 方式2：从本地配置文件读取（推荐）
try:
    from config_local import *  # 本地配置会覆盖上面的设置
except ImportError:
    pass

# ==================== 日志配置 ====================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"