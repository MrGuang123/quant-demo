# 🚀 量化交易系统 (Quantitative Trading System)

一个功能完整、模块化的量化交易框架，支持策略开发、回测、参数优化和实时信号监控。

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 目录

- [功能特性](#-功能特性)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [安装指南](#-安装指南)
- [使用教程](#-使用教程)
- [策略开发](#-策略开发)
- [配置说明](#-配置说明)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)

---

## ✨ 功能特性

### 核心功能
- ✅ **数据获取**：从主流交易所（Binance、OKX、Bybit等）获取实时和历史数据
- ✅ **技术指标**：内置50+常用技术指标（EMA、RSI、MACD、布林带等）
- ✅ **策略框架**：灵活的策略基类，易于扩展自定义策略
- ✅ **回测引擎**：基于VectorBT的高性能向量化回测
- ✅ **性能分析**：30+性能指标（夏普比率、最大回撤、盈亏比等）
- ✅ **参数优化**：网格搜索自动寻找最优参数
- ✅ **风险管理**：仓位管理、止损止盈、凯利公式
- ✅ **可视化**：交互式K线图、回测结果可视化、参数优化热力图

### 已实现策略
1. **EMA均线交叉策略** - 双均线金叉死叉
2. **RSI超买超卖策略** - 相对强弱指标
3. **MACD策略** - MACD指标金叉死叉
4. **MACD高级策略** - 结合零轴判断的增强版本

### 技术栈
- **数据获取**: CCXT
- **数据处理**: Pandas, NumPy
- **技术分析**: TA (Technical Analysis Library)
- **回测引擎**: VectorBT
- **可视化**: Matplotlib, Plotly, Seaborn
- **机器学习**: Scikit-learn (可选)

---

## 📁 项目结构

```
quant-demo/
├── README.md                 # 项目说明文档（本文件）
├── requirements.txt          # Python依赖包
├── config.py                 # 全局配置文件
├── .gitignore               # Git忽略文件
│
├── data/                     # 📊 数据模块
│   ├── __init__.py
│   ├── fetcher.py           # 数据获取（从交易所）
│   └── processor.py         # 数据处理（技术指标计算）
│
├── strategies/               # 📈 策略模块
│   ├── __init__.py
│   ├── base.py              # 策略基类
│   ├── ema_cross.py         # EMA交叉策略
│   ├── rsi_strategy.py      # RSI策略
│   └── macd_strategy.py     # MACD策略
│
├── backtest/                 # 🔬 回测模块
│   ├── __init__.py
│   ├── engine.py            # 回测引擎
│   └── metrics.py           # 性能指标计算
│
├── utils/                    # 🛠️ 工具模块
│   ├── __init__.py
│   ├── visualization.py     # 可视化工具
│   └── risk_manager.py      # 风险管理
│
├── examples/                 # 📚 示例脚本
│   ├── 01_simple_backtest.py      # 基础回测示例
│   ├── 02_multi_strategy.py       # 多策略对比
│   ├── 03_optimization.py         # 参数优化
│   └── 04_live_signal.py          # 实时信号监控
│
└── main.py                   # 🎯 主程序入口
```

---

## 🚀 快速开始

### 1. 克隆项目（或下载）

```bash
cd /path/to/your/projects
# 如果是新项目
mkdir quant-demo && cd quant-demo
```

### 2. 创建虚拟环境

```bash
# 使用 Python 3.10+ （推荐 3.12）
python3.12 -m venv .venv

# 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 运行第一个回测

```bash
# 运行示例1：简单回测
python examples/01_simple_backtest.py

# 运行示例2：多策略对比
python examples/02_multi_strategy.py

# 运行示例3：参数优化
python examples/03_optimization.py

# 运行示例4：实时信号监控
python examples/04_live_signal.py
```

---

## 💻 安装指南

### 系统要求

- **Python**: 3.10 或更高版本（推荐 3.12）
- **内存**: 至少 4GB RAM
- **磁盘**: 至少 500MB 可用空间

### 详细安装步骤

#### Step 1: 安装 Python

```bash
# macOS (使用 Homebrew)
brew install python@3.12

# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv

# Windows
# 从 python.org 下载安装包
```

#### Step 2: 创建项目虚拟环境

```bash
# 进入项目目录
cd quant-demo

# 创建虚拟环境
python3.12 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows
```

#### Step 3: 安装依赖包

```bash
# 升级 pip
pip install --upgrade pip

# 安装所有依赖
pip install -r requirements.txt

# 验证安装
python -c "import ccxt, pandas, vectorbt; print('✅ 所有依赖安装成功!')"
```

#### Step 4: （可选）安装 TA-Lib

TA-Lib 是一个强大的技术分析库，但需要先安装系统库：

```bash
# macOS
brew install ta-lib
pip install ta-lib

# Ubuntu/Debian
sudo apt-get install ta-lib
pip install ta-lib

# Windows
# 下载预编译包: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib‑0.4.XX‑cpXX‑cpXX‑win_amd64.whl
```

---

## 📖 使用教程

### 示例1：简单回测

```python
from data.fetcher import DataFetcher
from strategies.ema_cross import EMACrossStrategy
from backtest.engine import BacktestEngine

# 1. 获取数据
fetcher = DataFetcher("binance")
df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 1000)

# 2. 创建策略
strategy = EMACrossStrategy(fast_window=20, slow_window=60)

# 3. 回测
engine = BacktestEngine(initial_capital=10000, fees=0.0004)
results = engine.run(df, strategy)

# 4. 可视化
from utils.visualization import Visualizer
viz = Visualizer()
viz.plot_backtest_results(engine.get_portfolio(), df)
```

### 示例2：多策略对比

```python
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy

# 创建多个策略
strategies = [
    EMACrossStrategy(20, 60),
    RSIStrategy(14, 30, 70),
    MACDStrategy(12, 26, 9)
]

# 对比回测
comparison = engine.run_multiple_strategies(df, strategies)
print(comparison)
```

### 示例3：参数优化

```python
# 优化 EMA 策略的参数
best_params, best_result, results_df = engine.optimize_parameters(
    df,
    EMACrossStrategy,
    param_ranges={
        'fast_window': [10, 15, 20, 25, 30],
        'slow_window': [40, 50, 60, 70, 80]
    }
)

# 可视化优化结果
viz.plot_parameter_optimization(results_df, 'fast_window', 'slow_window')
```

### 示例4：实时信号监控

```python
import time

while True:
    # 获取最新数据
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 100, use_cache=False)
    
    # 生成信号
    entries, exits = strategy.generate_signals(df)
    
    # 检查最新信号
    if entries.iloc[-1]:
        print(f"🟢 买入信号! 价格: {df['close'].iloc[-1]}")
    elif exits.iloc[-1]:
        print(f"🔴 卖出信号! 价格: {df['close'].iloc[-1]}")
    
    # 等待下一个周期
    time.sleep(3600)  # 1小时
```

---

## 🎯 策略开发

### 创建自定义策略

所有策略都继承 `BaseStrategy` 类：

```python
from strategies.base import BaseStrategy
import pandas as pd
import ta

class MyCustomStrategy(BaseStrategy):
    """
    我的自定义策略
    """
    
    def __init__(self, param1=10, param2=20):
        super().__init__("我的策略")
        self.param1 = param1
        self.param2 = param2
        self.params = {
            'param1': param1,
            'param2': param2
        }
    
    def generate_signals(self, df: pd.DataFrame):
        """
        生成交易信号
        
        Returns:
            (entries, exits) - 买入和卖出信号的布尔Series
        """
        df = df.copy()
        
        # 计算你的指标
        df['indicator1'] = ta.trend.sma_indicator(df['close'], self.param1)
        df['indicator2'] = ta.trend.sma_indicator(df['close'], self.param2)
        
        # 生成信号
        entries = (df['indicator1'] > df['indicator2']) & \
                  (df['indicator1'].shift(1) <= df['indicator2'].shift(1))
        
        exits = (df['indicator1'] < df['indicator2']) & \
                (df['indicator1'].shift(1) >= df['indicator2'].shift(1))
        
        return entries, exits
```

### 使用自定义策略

```python
# 创建策略实例
my_strategy = MyCustomStrategy(param1=15, param2=30)

# 回测
results = engine.run(df, my_strategy)
```

---

## ⚙️ 配置说明

### config.py 主要配置项

```python
# 交易所配置
DEFAULT_EXCHANGE = "binance"      # 默认交易所
DEFAULT_SYMBOL = "BTC/USDT"       # 默认交易对
DEFAULT_TIMEFRAME = "1h"          # 默认时间周期

# 回测配置
INITIAL_CAPITAL = 10000           # 初始资金（USDT）
TRADING_FEE = 0.0004              # 交易手续费 0.04%
SLIPPAGE = 0.0001                 # 滑点 0.01%

# 风险管理
MAX_POSITION_SIZE = 0.95          # 最大仓位 95%
STOP_LOSS_PCT = 0.02              # 止损 2%
TAKE_PROFIT_PCT = 0.04            # 止盈 4%

# 数据配置
DATA_LIMIT = 1000                 # 默认K线数量
CACHE_ENABLED = True              # 启用缓存
```

### 修改配置

方法1：直接修改 `config.py`

方法2：创建 `config_local.py`（不会提交到Git）

```python
# config_local.py
DEFAULT_SYMBOL = "ETH/USDT"
INITIAL_CAPITAL = 50000
TRADING_FEE = 0.0002
```

---

## 📊 性能指标说明

系统计算的主要指标：

| 指标 | 说明 | 好的范围 |
|-----|-----|---------|
| **总收益率** | 累计收益百分比 | > 0% |
| **年化收益** | 按年计算的收益率 | > 10% |
| **夏普比率** | 风险调整后的收益 | > 1.0（越高越好）|
| **最大回撤** | 最大亏损幅度 | < 20% |
| **索提诺比率** | 只考虑下行风险的夏普 | > 1.0 |
| **卡玛比率** | 年化收益/最大回撤 | > 1.0 |
| **胜率** | 盈利交易占比 | > 50% |
| **盈亏比** | 平均盈利/平均亏损 | > 1.5 |
| **交易次数** | 总交易次数 | 适中（不要过度交易）|

---

## 🔧 常见问题

### Q1: 如何切换不同的交易所？

```python
# 支持的交易所：binance, okx, bybit, coinbase 等
fetcher = DataFetcher("okx")
df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 1000)
```

### Q2: 数据缓存在哪里？

缓存文件在 `data/cache/` 目录下。清空缓存：

```python
fetcher.clear_cache()
```

### Q3: 如何使用更高的时间周期？

```python
# 支持的周期: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
df = fetcher.fetch_ohlcv("BTC/USDT", "4h", 500)
```

### Q4: 回测速度慢怎么办？

1. 减少数据量（limit参数）
2. 使用缓存（use_cache=True）
3. 优化策略代码（避免循环）
4. 使用更快的硬件

### Q5: 如何接入实盘交易？

**警告**：实盘交易有风险，请谨慎！

```python
# 1. 在 config.py 中设置API密钥
BINANCE_API_KEY = "your_api_key"
BINANCE_API_SECRET = "your_api_secret"

# 2. 使用认证的交易所实例
exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET
})

# 3. 下单（示例）
# order = exchange.create_market_buy_order('BTC/USDT', 0.001)
```

### Q6: Python 版本问题

- **最低要求**: Python 3.10
- **推荐版本**: Python 3.12
- **避免使用**: Python 3.9（很多库不再支持）

---

## 📈 性能优化建议

1. **数据处理**
   - 使用向量化操作（避免 for 循环）
   - 合理使用缓存
   - 减少不必要的数据复制

2. **回测优化**
   - 使用 VectorBT 的并行计算
   - 减少参数优化的搜索空间
   - 使用更大的时间周期（如4h代替1h）

3. **策略开发**
   - 避免过拟合（参数不要太多）
   - 使用样本外测试
   - 考虑交易成本和滑点

---

## 🤝 贡献指南

欢迎贡献代码、报告Bug或提出新功能建议！

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 使用 PEP 8 代码风格
- 添加类型注解
- 编写文档字符串
- 添加单元测试

---

## 📚 学习资源

### 推荐书籍
- 《量化投资：以Python为工具》
- 《Python金融大数据分析》
- 《算法交易：制胜策略与原理》

### 推荐网站
- [QuantConnect](https://www.quantconnect.com/) - 量化平台
- [Backtrader](https://www.backtrader.com/) - 回测框架
- [TradingView](https://www.tradingview.com/) - 图表和指标

### 相关库文档
- [CCXT文档](https://docs.ccxt.com/)
- [VectorBT文档](https://vectorbt.dev/)
- [Pandas文档](https://pandas.pydata.org/)

---

## ⚠️ 免责声明

**本项目仅供学习和研究使用，不构成任何投资建议。**

- 量化交易有风险，投资需谨慎
- 历史回测结果不代表未来表现
- 作者不对任何投资损失负责
- 请在充分理解的基础上使用本系统
- 实盘交易前请务必进行充分测试

---

## 📄 开源协议

本项目采用 MIT 协议开源。详见 [LICENSE](LICENSE) 文件。

---

## 📮 联系方式

- **问题反馈**: 在 GitHub Issues 提交
- **功能建议**: 在 GitHub Discussions 讨论
- **邮箱**: your-email@example.com

---

## 🌟 Star History

如果这个项目对你有帮助，请给一个 ⭐️ Star！

---

## 🎉 致谢

感谢以下开源项目：
- [CCXT](https://github.com/ccxt/ccxt) - 统一的交易所API
- [VectorBT](https://github.com/polakowo/vectorbt) - 高性能回测框架
- [TA](https://github.com/bukosabino/ta) - 技术分析库
- [Plotly](https://plotly.com/) - 交互式可视化

---

**Happy Trading! 📈💰**

*最后更新: 2026-02-02*
