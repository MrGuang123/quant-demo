"""
示例1: 简单回测
演示如何使用框架进行基础的策略回测
"""
import sys
sys.path.append('..')  # 添加父目录到路径

from data.fetcher import DataFetcher
from data.processor import DataProcessor
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from backtest.engine import BacktestEngine
from utils.visualization import Visualizer
import config


def main():
    """主函数"""
    print("=" * 80)
    print("示例1: 简单回测演示")
    print("=" * 80)
    
    # ==================== 1. 获取数据 ====================
    print("\n📊 步骤1: 获取数据...")
    fetcher = DataFetcher(config.DEFAULT_EXCHANGE)
    df = fetcher.fetch_ohlcv(
        symbol=f"{config.DEFAULT_SYMBOL}",
        timeframe=config.DEFAULT_TIMEFRAME,
        limit=1000
    )
    
    print(f"✅ 数据获取成功: {len(df)} 根K线")
    print(f"时间范围: {df['timestamp'].min()} 到 {df['timestamp'].max()}")
    
    # ==================== 2. 数据处理（可选）====================
    print("\n📊 步骤2: 数据处理...")
    processor = DataProcessor()
    df = processor.add_technical_indicators(df, indicators=['ema', 'rsi', 'macd'])
    df = processor.clean_data(df)
    print("✅ 技术指标计算完成")
    
    # ==================== 3. 创建策略 ====================
    print("\n🎯 步骤3: 创建交易策略...")
    
    # 选择一个策略进行回测
    # 方式1: EMA交叉策略
    strategy = EMACrossStrategy(fast_window=20, slow_window=60)
    
    # 方式2: RSI策略（注释掉的备选）
    # strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    
    # 方式3: MACD策略（注释掉的备选）
    # strategy = MACDStrategy(fast=12, slow=26, signal=9)
    
    print(f"✅ 策略创建成功: {strategy}")
    
    # ==================== 4. 运行回测 ====================
    print("\n🚀 步骤4: 开始回测...")
    
    engine = BacktestEngine(
        initial_capital=10000,  # 初始资金10000 USDT
        fees=0.0004,           # 手续费0.04%
        slippage=0.0001        # 滑点0.01%
    )
    
    results = engine.run(df, strategy)
    
    # ==================== 5. 可视化结果 ====================
    print("\n📈 步骤5: 可视化回测结果...")
    
    viz = Visualizer()
    
    # 生成信号用于可视化
    entries, exits = strategy.generate_signals(df)
    
    # 绘制K线图和交易信号
    print("绘制K线图...")
    viz.plot_candlestick(
        df,
        title=f"{strategy.name} - BTC/USDT 1H",
        signals={'entries': entries, 'exits': exits}
    )
    
    # 绘制回测结果（权益曲线和回撤）
    print("绘制回测结果...")
    portfolio = engine.get_portfolio()
    viz.plot_backtest_results(portfolio, df)
    
    # ==================== 6. 结果分析 ====================
    print("\n📊 步骤6: 结果分析")
    print("-" * 60)
    
    if results['total_return'] > 0:
        print("✅ 策略盈利")
        print(f"   总收益: {results['total_return']:.2%}")
        print(f"   年化收益: {results['annual_return']:.2%}")
    else:
        print("❌ 策略亏损")
        print(f"   总收益: {results['total_return']:.2%}")
    
    print(f"\n风险评估:")
    print(f"   夏普比率: {results['sharpe_ratio']:.2f} ({'优秀' if results['sharpe_ratio'] > 1 else '一般' if results['sharpe_ratio'] > 0 else '差'})")
    print(f"   最大回撤: {results['max_drawdown']:.2%}")
    print(f"   胜率: {results['win_rate']:.2%}")
    
    print(f"\n交易统计:")
    print(f"   总交易: {results['total_trades']} 次")
    print(f"   盈利交易: {results['winning_trades']} 次")
    print(f"   亏损交易: {results['losing_trades']} 次")
    
    print("\n" + "=" * 80)
    print("回测完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()