# 🚀 命令速查表 (Cheat Sheet)

快速参考常用命令和代码片段。

---

## 📦 环境管理

```bash
# 创建虚拟环境
python3.12 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate             # Windows

# 退出虚拟环境
deactivate

# 安装依赖
pip install -r requirements.txt

# 导出依赖
pip freeze > requirements.txt

# 清理缓存
rm -rf data/cache/
```

---

## 🧪 测试命令

```bash
# 测试安装
python test_installation.py

# 运行示例
python examples/01_simple_backtest.py
python examples/02_multi_strategy.py
python examples/03_optimization.py
python examples/04_live_signal.py

# 运行主程序
python main.py
```

---

## 📊 数据获取

```python
from data.fetcher import DataFetcher

# 创建获取器
fetcher = DataFetcher("binance")  # binance, okx, bybit

# 获取单个交易对
df = fetcher.fetch_ohlcv(
    symbol="BTC/USDT",     # 交易对
    timeframe="1h",        # 1m, 5m, 15m, 1h, 4h, 1d, 1w
    limit=1000,            # K线数量
    use_cache=True         # 使用缓存
)

# 获取多个交易对
data = fetcher.fetch_multiple_symbols(
    ["BTC/USDT", "ETH/USDT", "BNB/USDT"],
    "1h",
    500
)

# 清空缓存
fetcher.clear_cache()
```

---

## 📈 策略使用

```python
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy

# 创建策略
strategy = EMACrossStrategy(fast_window=20, slow_window=60)
strategy = RSIStrategy(period=14, oversold=30, overbought=70)
strategy = MACDStrategy(fast=12, slow=26, signal=9)

# 生成信号
entries, exits = strategy.generate_signals(df)

# 查看信号
print(f"买入信号: {entries.sum()}")
print(f"卖出信号: {exits.sum()}")
```

---

## 🔬 回测引擎

```python
from backtest.engine import BacktestEngine

# 创建引擎
engine = BacktestEngine(
    initial_capital=10000,  # 初始资金
    fees=0.0004,            # 手续费 0.04%
    slippage=0.0001         # 滑点 0.01%
)

# 单策略回测
results = engine.run(df, strategy)

# 多策略对比
strategies = [strategy1, strategy2, strategy3]
comparison = engine.run_multiple_strategies(df, strategies)

# 参数优化
best_params, best_result, results_df = engine.optimize_parameters(
    df,
    EMACrossStrategy,
    param_ranges={
        'fast_window': [10, 20, 30],
        'slow_window': [40, 60, 80]
    }
)
```

---

## 📊 性能指标

```python
# 查看结果
print(f"总收益率: {results['total_return']:.2%}")
print(f"年化收益: {results['annual_return']:.2%}")
print(f"夏普比率: {results['sharpe_ratio']:.2f}")
print(f"最大回撤: {results['max_drawdown']:.2%}")
print(f"胜率: {results['win_rate']:.2%}")
print(f"盈亏比: {results['profit_factor']:.2f}")
print(f"交易次数: {results['total_trades']}")

# 获取权益曲线
portfolio = engine.get_portfolio()
equity = portfolio.value()
drawdown = portfolio.drawdown()

# 获取交易记录
trades = portfolio.trades.records_readable
```

---

## 🎨 可视化

```python
from utils.visualization import Visualizer

viz = Visualizer()

# K线图
viz.plot_candlestick(
    df,
    title="BTC/USDT K线图",
    show_volume=True,
    signals={'entries': entries, 'exits': exits}
)

# 策略信号
viz.plot_strategy_signals(
    df, entries, exits,
    indicators={'EMA20': 'ema_fast', 'EMA60': 'ema_slow'}
)

# 回测结果
viz.plot_backtest_results(portfolio, df)

# 参数优化热力图
viz.plot_parameter_optimization(
    results_df,
    'fast_window',
    'slow_window'
)
```

---

## 🛡️ 风险管理

```python
from utils.risk_manager import RiskManager

# 创建风险管理器
rm = RiskManager(
    max_position_size=0.95,  # 最大仓位95%
    stop_loss_pct=0.02,      # 止损2%
    take_profit_pct=0.04     # 止盈4%
)

# 计算仓位
position_size = rm.calculate_position_size(
    capital=10000,
    entry_price=50000,
    risk_per_trade=0.02
)

# 计算止损止盈
stop_loss = rm.calculate_stop_loss(entry_price=50000)
take_profit = rm.calculate_take_profit(entry_price=50000)

# 凯利公式
kelly = rm.calculate_kelly_criterion(
    win_rate=0.55,
    avg_win=0.02,
    avg_loss=0.01
)
```

---

## 🔧 配置修改

```python
# config.py 主要参数

# 交易所
DEFAULT_EXCHANGE = "binance"
DEFAULT_SYMBOL = "BTC/USDT"
DEFAULT_TIMEFRAME = "1h"

# 回测
INITIAL_CAPITAL = 10000
TRADING_FEE = 0.0004
SLIPPAGE = 0.0001

# 策略参数
EMA_FAST_WINDOW = 20
EMA_SLOW_WINDOW = 60
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# 风险管理
MAX_POSITION_SIZE = 0.95
STOP_LOSS_PCT = 0.02
TAKE_PROFIT_PCT = 0.04

# 数据
DATA_LIMIT = 1000
CACHE_ENABLED = True
```

---

## 📝 创建自定义策略

```python
from strategies.base import BaseStrategy
import pandas as pd
import ta

class MyStrategy(BaseStrategy):
    def __init__(self, param1=10):
        super().__init__("我的策略")
        self.param1 = param1
        self.params = {'param1': param1}
    
    def generate_signals(self, df: pd.DataFrame):
        df = df.copy()
        
        # 计算指标
        df['indicator'] = ta.trend.sma_indicator(df['close'], self.param1)
        
        # 生成信号
        entries = (df['close'] > df['indicator']) & \
                  (df['close'].shift(1) <= df['indicator'].shift(1))
        exits = (df['close'] < df['indicator']) & \
                (df['close'].shift(1) >= df['indicator'].shift(1))
        
        return entries, exits
```

---

## 🚀 完整流程模板

```python
# 1. 导入模块
from data.fetcher import DataFetcher
from strategies.ema_cross import EMACrossStrategy
from backtest.engine import BacktestEngine
from utils.visualization import Visualizer

# 2. 获取数据
fetcher = DataFetcher("binance")
df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 1000)

# 3. 创建策略
strategy = EMACrossStrategy(20, 60)

# 4. 回测
engine = BacktestEngine(initial_capital=10000, fees=0.0004)
results = engine.run(df, strategy)

# 5. 可视化
viz = Visualizer()
viz.plot_backtest_results(engine.get_portfolio(), df)

# 6. 优化（可选）
best_params, _, _ = engine.optimize_parameters(
    df, EMACrossStrategy,
    {'fast_window': [10, 20, 30], 'slow_window': [40, 60, 80]}
)
```

---

## 🔍 调试技巧

```python
# 查看数据
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())

# 查看信号
print(df[entries])  # 买入点
print(df[exits])    # 卖出点

# 查看最新价格
print(f"最新价格: {df['close'].iloc[-1]}")

# 查看交易记录
trades = portfolio.trades.records_readable
print(trades[['Entry Date', 'Exit Date', 'PnL', 'Return']])

# 查看策略参数
print(strategy.get_params())
```

---

## 📱 实时监控模板

```python
import time
from datetime import datetime

fetcher = DataFetcher("binance")
strategy = EMACrossStrategy(20, 60)

while True:
    try:
        # 获取最新数据
        df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 100, use_cache=False)
        
        # 生成信号
        entries, exits = strategy.generate_signals(df)
        
        # 检查信号
        if entries.iloc[-1]:
            print(f"🟢 买入信号! 价格: ${df['close'].iloc[-1]:,.2f}")
        elif exits.iloc[-1]:
            print(f"🔴 卖出信号! 价格: ${df['close'].iloc[-1]:,.2f}")
        else:
            print(f"⚪ 持仓不变  价格: ${df['close'].iloc[-1]:,.2f}")
        
        # 等待下一个周期
        time.sleep(3600)  # 1小时
        
    except KeyboardInterrupt:
        print("\n程序已停止")
        break
    except Exception as e:
        print(f"错误: {e}")
        time.sleep(60)
```

---

## 📊 常用技术指标

```python
import ta

# 趋势指标
df['sma'] = ta.trend.sma_indicator(df['close'], window=20)
df['ema'] = ta.trend.ema_indicator(df['close'], window=20)
df['macd'] = ta.trend.MACD(df['close']).macd()
df['macd_signal'] = ta.trend.MACD(df['close']).macd_signal()

# 动量指标
df['rsi'] = ta.momentum.rsi(df['close'], window=14)
df['stoch'] = ta.momentum.stoch(df['high'], df['low'], df['close'])

# 波动率指标
df['bb_high'] = ta.volatility.bollinger_hband(df['close'])
df['bb_low'] = ta.volatility.bollinger_lband(df['close'])
df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])

# 成交量指标
df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
df['vwap'] = ta.volume.volume_weighted_average_price(
    df['high'], df['low'], df['close'], df['volume']
)
```

---

## 🎯 性能评估标准

```python
# 优秀策略的特征
results['sharpe_ratio'] > 1.5        # 夏普比率 > 1.5
results['max_drawdown'] < 0.15       # 最大回撤 < 15%
results['win_rate'] > 0.50           # 胜率 > 50%
results['profit_factor'] > 2.0       # 盈亏比 > 2.0
results['total_return'] > 0.20       # 总收益 > 20%
```

---

## 💡 快速提示

```bash
# 查看Python版本
python --version

# 查看pip版本
pip --version

# 查看已安装的包
pip list

# 查看某个包的信息
pip show ccxt

# 更新某个包
pip install --upgrade ccxt

# 查看项目结构
tree -L 2 -I '.venv|__pycache__'

# 统计代码行数
find . -name "*.py" -not -path "./.venv/*" | xargs wc -l
```

---

## 🆘 紧急救援

```bash
# 虚拟环境问题
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 清空缓存
rm -rf data/cache/
rm -rf __pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} +

# 重新安装某个包
pip uninstall vectorbt
pip install vectorbt

# 查看错误详情
python -v script.py  # verbose模式
```

---

**保存这个文件，随时查阅！** 📚

*提示：用 Ctrl+F 快速搜索你需要的命令*
