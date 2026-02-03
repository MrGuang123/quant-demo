# 🎯 开始使用 - 3步上手

欢迎使用量化交易系统！这个指南会帮你在10分钟内完成设置并运行第一个回测。

---

## ⚡ 快速开始（仅需3步）

### 步骤1：安装依赖（5分钟）

```bash
# 1. 进入项目目录
cd quant-demo

# 2. 创建虚拟环境（如果还没有）
python3.12 -m venv .venv

# 3. 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或者
.venv\Scripts\activate     # Windows

# 4. 升级pip
pip install --upgrade pip

# 5. 安装所有依赖
pip install -r requirements.txt
```

等待安装完成...（可能需要3-5分钟）

### 步骤2：测试安装（1分钟）

```bash
# 运行安装测试脚本
python test_installation.py
```

如果看到 `🎉 所有测试通过！系统已就绪！`，说明安装成功！

### 步骤3：运行第一个回测（2分钟）

```bash
# 运行示例1：简单回测
python examples/01_simple_backtest.py
```

你会看到回测结果和图表！🎉

---

## 📚 接下来做什么？

### 选项A：查看更多示例

```bash
# 示例2：多策略对比
python examples/02_multi_strategy.py

# 示例3：参数优化
python examples/03_optimization.py

# 示例4：实时信号监控
python examples/04_live_signal.py
```

### 选项B：阅读文档

1. **快速入门**：`QUICKSTART.md` - 5分钟上手指南
2. **完整文档**：`README.md` - 项目完整说明
3. **中文教程**：`TUTORIAL_CN.md` - 详细的中文教程

### 选项C：开始开发

1. 查看现有策略：`strategies/` 目录
2. 复制一个策略文件作为模板
3. 修改策略逻辑
4. 运行回测验证

---

## 🐛 遇到问题？

### 常见问题

**Q: pip install 很慢？**
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: 提示 ModuleNotFoundError？**
```bash
# 确保虚拟环境已激活
source .venv/bin/activate
which python  # 应该显示 .venv/bin/python

# 重新安装依赖
pip install -r requirements.txt
```

**Q: 数据获取失败？**
```bash
# 检查网络连接
# 或者使用缓存的数据（修改 config.py: CACHE_ENABLED = True）
```

**Q: Python版本太低？**
```bash
# 检查Python版本
python --version  # 需要 >= 3.10

# 安装新版本Python
# macOS: brew install python@3.12
# Ubuntu: sudo apt install python3.12
```

---

## 📖 推荐学习路径

### 第1天：熟悉环境
- ✅ 完成安装
- ✅ 运行所有示例
- ✅ 查看代码结构

### 第2-3天：理解概念
- ✅ 阅读 `TUTORIAL_CN.md`
- ✅ 理解OHLCV数据
- ✅ 学习技术指标

### 第4-7天：实践操作
- ✅ 修改策略参数
- ✅ 测试不同币种
- ✅ 分析回测结果

### 第2周：开发策略
- ✅ 创建自己的策略
- ✅ 参数优化
- ✅ 风险管理

---

## 🎓 学习资源

### 视频教程（推荐）
- YouTube: 搜索 "Python量化交易"
- Bilibili: 搜索 "量化交易回测"

### 在线课程
- Coursera: Machine Learning
- Udemy: Algorithmic Trading

### 书籍推荐
- 《Python金融大数据分析》
- 《量化投资：以Python为工具》
- 《算法交易：制胜策略与原理》

---

## 🎯 项目结构速览

```
quant-demo/
├── 📄 文档
│   ├── README.md           # 完整项目说明
│   ├── QUICKSTART.md       # 5分钟快速开始
│   ├── TUTORIAL_CN.md      # 详细中文教程
│   └── GETTING_STARTED.md  # 本文件
│
├── 🧪 测试
│   └── test_installation.py # 安装测试脚本
│
├── ⚙️ 配置
│   ├── config.py            # 全局配置
│   ├── config_example.py    # 配置示例
│   └── requirements.txt     # Python依赖
│
├── 📊 数据模块
│   └── data/
│       ├── fetcher.py       # 从交易所获取数据
│       └── processor.py     # 数据处理和指标计算
│
├── 📈 策略模块
│   └── strategies/
│       ├── base.py          # 策略基类
│       ├── ema_cross.py     # EMA交叉策略
│       ├── rsi_strategy.py  # RSI策略
│       └── macd_strategy.py # MACD策略
│
├── 🔬 回测模块
│   └── backtest/
│       ├── engine.py        # 回测引擎
│       └── metrics.py       # 性能指标
│
├── 🛠️ 工具模块
│   └── utils/
│       ├── visualization.py # 图表可视化
│       └── risk_manager.py  # 风险管理
│
└── 📚 示例脚本
    └── examples/
        ├── 01_simple_backtest.py  # 基础回测
        ├── 02_multi_strategy.py   # 多策略对比
        ├── 03_optimization.py     # 参数优化
        └── 04_live_signal.py      # 实时监控
```

---

## 💡 小提示

1. **从简单开始**
   - 先运行示例，理解流程
   - 不要急于实盘交易
   - 多做回测和分析

2. **保持学习**
   - 量化交易是个长期过程
   - 持续学习新方法
   - 记录和总结经验

3. **风险控制**
   - 永远不要用借来的钱交易
   - 只用能承受损失的资金
   - 设置止损，控制风险

4. **社区交流**
   - 在GitHub提Issue
   - 分享你的经验
   - 帮助其他学习者

---

## 🚀 准备好了吗？

现在运行你的第一个回测：

```bash
python examples/01_simple_backtest.py
```

**祝你交易顺利！📈💰**

---

*有问题？查看 `TUTORIAL_CN.md` 获取详细帮助！*
