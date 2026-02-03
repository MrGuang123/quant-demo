"""
示例3: 参数优化
寻找策略的最优参数组合
"""
import sys
sys.path.append('..')

from data.fetcher import DataFetcher
from data.processor import DataProcessor
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from backtest.engine import BacktestEngine
from utils.visualization import Visualizer
import pandas as pd


def optimize_ema_strategy():
    """优化EMA交叉策略"""
    print("=" * 80)
    print("示例3A: EMA策略参数优化")
    print("=" * 80)
    
    # 获取数据
    fetcher = DataFetcher("binance")
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 2000)
    
    processor = DataProcessor()
    df = processor.clean_data(df)
    
    # 创建回测引擎
    engine = BacktestEngine(initial_capital=10000, fees=0.0004)
    
    # 定义参数搜索空间
    param_ranges = {
        'fast_window': [10, 15, 20, 25, 30],
        'slow_window': [40, 50, 60, 70, 80]
    }
    
    # 运行优化
    best_params, best_result, results_df = engine.optimize_parameters(
        df=df,
        strategy_class=EMACrossStrategy,
        param_ranges=param_ranges
    )
    
    # 保存优化结果
    output_file = "../results/ema_optimization.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n💾 优化结果已保存: {output_file}")
    
    # 可视化优化结果（热力图）
    if len(param_ranges) == 2:
        viz = Visualizer()
        param_names = list(param_ranges.keys())
        viz.plot_parameter_optimization(results_df, param_names[0], param_names[1])
    
    return best_params, best_result


def optimize_rsi_strategy():
    """优化RSI策略"""
    print("\n" + "=" * 80)
    print("示例3B: RSI策略参数优化")
    print("=" * 80)
    
    # 获取数据
    fetcher = DataFetcher("binance")
    df = fetcher.fetch_ohlcv("ETH/USDT", "4h", 1000)
    
    processor = DataProcessor()
    df = processor.clean_data(df)
    
    # 创建回测引擎
    engine = BacktestEngine(initial_capital=10000, fees=0.0004)
    
    # 定义参数搜索空间
    param_ranges = {
        'period': [10, 14, 20],
        'oversold': [20, 25, 30, 35],
        'overbought': [65, 70, 75, 80]
    }
    
    # 运行优化
    best_params, best_result, results_df = engine.optimize_parameters(
        df=df,
        strategy_class=RSIStrategy,
        param_ranges=param_ranges
    )
    
    # 保存结果
    output_file = "../results/rsi_optimization.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n💾 优化结果已保存: {output_file}")
    
    return best_params, best_result


def walk_forward_analysis():
    """
    步进式分析（Walk-Forward Analysis）
    将数据分为训练集和测试集，避免过拟合
    """
    print("\n" + "=" * 80)
    print("示例3C: 步进式分析（防止过拟合）")
    print("=" * 80)
    
    # 获取较长时间的数据
    fetcher = DataFetcher("binance")
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 3000)
    
    processor = DataProcessor()
    df = processor.clean_data(df)
    
    # 分割数据：70%训练，30%测试
    train_size = int(len(df) * 0.7)
    df_train = df.iloc[:train_size].copy()
    df_test = df.iloc[train_size:].copy()
    
    print(f"训练集: {len(df_train)} 根K线")
    print(f"测试集: {len(df_test)} 根K线")
    
    # 在训练集上优化参数
    print("\n🔍 在训练集上寻找最优参数...")
    engine = BacktestEngine(initial_capital=10000, fees=0.0004)
    
    param_ranges = {
        'fast_window': [15, 20, 25],
        'slow_window': [50, 60, 70]
    }
    
    best_params, _, _ = engine.optimize_parameters(
        df=df_train,
        strategy_class=EMACrossStrategy,
        param_ranges=param_ranges
    )
    
    # 在测试集上验证
    print("\n✅ 使用最优参数在测试集上验证...")
    strategy = EMACrossStrategy(**best_params)
    
    test_results = engine.run(df_test, strategy)
    
    print("\n" + "=" * 80)
    print("🎯 步进式分析总结")
    print("=" * 80)
    print(f"最优参数: {best_params}")
    print(f"测试集表现:")
    print(f"  - 总收益: {test_results['total_return']:.2%}")
    print(f"  - 夏普比率: {test_results['sharpe_ratio']:.2f}")
    print(f"  - 最大回撤: {test_results['max_drawdown']:.2%}")
    print(f"  - 胜率: {test_results['win_rate']:.2%}")
    
    if test_results['sharpe_ratio'] > 1.0:
        print("\n✅ 策略在测试集上表现良好，可能具有实战价值")
    else:
        print("\n⚠️  策略在测试集上表现一般，可能存在过拟合")


def main():
    """主函数"""
    print("开始参数优化示例...\n")
    
    # 选择运行哪个优化示例
    print("请选择优化示例:")
    print("1. EMA策略优化")
    print("2. RSI策略优化")
    print("3. 步进式分析（推荐）")
    print("4. 全部运行")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == "1":
        optimize_ema_strategy()
    elif choice == "2":
        optimize_rsi_strategy()
    elif choice == "3":
        walk_forward_analysis()
    elif choice == "4":
        optimize_ema_strategy()
        optimize_rsi_strategy()
        walk_forward_analysis()
    else:
        print("默认运行步进式分析...")
        walk_forward_analysis()
    
    print("\n✅ 所有优化完成！")


if __name__ == "__main__":
    main()