"""
量化交易系统 - 主程序
快速开始使用量化交易框架
"""
import ccxt
import pandas as pd
import ta
import vectorbt as vbt

# 导入自定义模块
from data.fetcher import DataFetcher
from data.processor import DataProcessor
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from backtest.engine import BacktestEngine
from utils.visualization import Visualizer
from utils.risk_manager import RiskManager
import config


def quick_start():
    """
    快速开始 - 简单的回测示例
    """
    print("=" * 80)
    print("🚀 量化交易系统 - 快速开始")
    print("=" * 80)
    
    # 1. 获取数据
    print("\n📊 步骤1: 获取数据...")
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 1000)
    print(f"✅ 获取了 {len(df)} 根K线")
    
    # 2. 创建策略
    print("\n🎯 步骤2: 创建策略...")
    strategy = EMACrossStrategy(fast_window=20, slow_window=60)
    print(f"✅ 策略: {strategy}")
    
    # 3. 运行回测
    print("\n🚀 步骤3: 运行回测...")
    engine = BacktestEngine(
        initial_capital=10000,
        fees=0.0004
    )
    results = engine.run(df, strategy)
    
    # 4. 可视化
    print("\n📈 步骤4: 可视化结果...")
    entries, exits = strategy.generate_signals(df)
    
    viz = Visualizer()
    viz.plot_candlestick(
        df,
        title=f"{strategy.name} 回测结果",
        signals={'entries': entries, 'exits': exits}
    )
    
    portfolio = engine.get_portfolio()
    viz.plot_backtest_results(portfolio, df)
    
    print("\n✅ 完成！")


def main_menu():
    """主菜单"""
    while True:
        print("\n" + "=" * 80)
        print("量化交易系统 - 主菜单")
        print("=" * 80)
        print("1. 快速开始（简单回测）")
        print("2. 单策略回测")
        print("3. 多策略对比")
        print("4. 参数优化")
        print("5. 实时信号监控")
        print("6. 数据查看与分析")
        print("0. 退出")
        print("=" * 80)
        
        choice = input("\n请选择功能 (0-6): ").strip()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice == "1":
            quick_start()
        elif choice == "2":
            single_strategy_backtest()
        elif choice == "3":
            multi_strategy_comparison()
        elif choice == "4":
            parameter_optimization()
        elif choice == "5":
            live_monitoring()
        elif choice == "6":
            data_analysis()
        else:
            print("❌ 无效选项，请重新选择")


def single_strategy_backtest():
    """单策略回测"""
    print("\n" + "=" * 80)
    print("单策略回测")
    print("=" * 80)
    
    # 选择交易对
    symbol = input("请输入交易对 (默认 BTC/USDT): ").strip() or "BTC/USDT"
    
    # 选择周期
    print("\n时间周期: 1. 1h  2. 4h  3. 1d")
    tf_choice = input("请选择 (默认1): ").strip() or "1"
    timeframes = {"1": "1h", "2": "4h", "3": "1d"}
    timeframe = timeframes.get(tf_choice, "1h")
    
    # 选择策略
    print("\n策略类型:")
    print("1. EMA交叉策略")
    print("2. RSI策略")
    print("3. MACD策略")
    strategy_choice = input("请选择 (默认1): ").strip() or "1"
    
    if strategy_choice == "1":
        fast = int(input("快线周期 (默认20): ").strip() or "20")
        slow = int(input("慢线周期 (默认60): ").strip() or "60")
        strategy = EMACrossStrategy(fast_window=fast, slow_window=slow)
    elif strategy_choice == "2":
        period = int(input("RSI周期 (默认14): ").strip() or "14")
        oversold = int(input("超卖线 (默认30): ").strip() or "30")
        overbought = int(input("超买线 (默认70): ").strip() or "70")
        strategy = RSIStrategy(period=period, oversold=oversold, overbought=overbought)
    else:
        strategy = MACDStrategy()
    
    # 执行回测
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv(symbol, timeframe, 1000)
    
    engine = BacktestEngine()
    results = engine.run(df, strategy)
    
    # 可视化
    entries, exits = strategy.generate_signals(df)
    viz = Visualizer()
    viz.plot_candlestick(df, title=f"{symbol} {timeframe}", signals={'entries': entries, 'exits': exits})
    viz.plot_backtest_results(engine.get_portfolio(), df)


def multi_strategy_comparison():
    """多策略对比"""
    from examples.multi_strategy import main as multi_main
    multi_main()


def parameter_optimization():
    """参数优化"""
    from examples.optimization import main as opt_main
    opt_main()


def live_monitoring():
    """实时监控"""
    from examples.live_signal import main as live_main
    live_main()


def data_analysis():
    """数据分析"""
    print("\n" + "=" * 80)
    print("数据查看与分析")
    print("=" * 80)
    
    symbol = input("请输入交易对 (默认 BTC/USDT): ").strip() or "BTC/USDT"
    timeframe = input("请输入周期 (默认 1h): ").strip() or "1h"
    limit = int(input("请输入K线数量 (默认500): ").strip() or "500")
    
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv(symbol, timeframe, limit)
    
    processor = DataProcessor()
    df = processor.add_technical_indicators(df)
    df = processor.calculate_returns(df)
    
    print("\n数据概览:")
    print(df.describe())
    
    print("\n最近10根K线:")
    print(df[['timestamp', 'close', 'volume', 'rsi', 'ema_12', 'ema_26']].tail(10))
    
    # 可视化
    viz = Visualizer()
    viz.plot_candlestick(df, title=f"{symbol} {timeframe} 数据分析")


if __name__ == "__main__":
    # 直接运行快速开始
    # quick_start()
    
    # 或者显示菜单
    main_menu()