"""
示例2: 多策略对比
对比不同策略在同一数据上的表现
"""
import sys
sys.path.append('..')

from data.fetcher import DataFetcher
from data.processor import DataProcessor
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy, MACDAdvancedStrategy
from backtest.engine import BacktestEngine
import pandas as pd


def main():
    """主函数"""
    print("=" * 80)
    print("示例2: 多策略对比")
    print("=" * 80)
    
    # ==================== 1. 获取数据 ====================
    print("\n📊 获取数据...")
    fetcher = DataFetcher("binance")
    df = fetcher.fetch_ohlcv("BTC/USDT", "4h", 1000)  # 使用4小时周期
    
    processor = DataProcessor()
    df = processor.add_technical_indicators(df)
    df = processor.clean_data(df)
    
    print(f"✅ 数据准备完成: {len(df)} 根K线")
    
    # ==================== 2. 创建多个策略 ====================
    print("\n🎯 创建策略组合...")
    
    strategies = [
        # EMA交叉策略 - 不同参数组合
        EMACrossStrategy(fast_window=12, slow_window=26),
        EMACrossStrategy(fast_window=20, slow_window=60),
        EMACrossStrategy(fast_window=50, slow_window=200),
        
        # RSI策略 - 不同参数组合
        RSIStrategy(period=14, oversold=30, overbought=70),
        RSIStrategy(period=14, oversold=20, overbought=80),
        
        # MACD策略
        MACDStrategy(fast=12, slow=26, signal=9),
        MACDAdvancedStrategy(fast=12, slow=26, signal=9),
    ]
    
    print(f"✅ 创建了 {len(strategies)} 个策略")
    
    # ==================== 3. 批量回测 ====================
    print("\n🚀 开始批量回测...")
    
    engine = BacktestEngine(
        initial_capital=10000,
        fees=0.0004
    )
    
    # 运行所有策略
    comparison_df = engine.run_multiple_strategies(df, strategies)
    
    # ==================== 4. 保存结果 ====================
    output_file = "../results/strategy_comparison.csv"
    comparison_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 结果已保存到: {output_file}")
    
    # ==================== 5. 分析最佳策略 ====================
    print("\n" + "=" * 80)
    print("🏆 推荐策略")
    print("=" * 80)
    
    # 根据不同维度推荐
    print("\n📈 按总收益排名:")
    # 注意：这里需要处理百分比字符串，实际使用时可以优化
    print(comparison_df.nlargest(3, '策略名称')[['策略名称', '总收益率', '最大回撤']].to_string(index=False))
    
    print("\n💎 按夏普比率排名（风险调整后收益）:")
    print(comparison_df.nlargest(3, '策略名称')[['策略名称', '夏普比率', '年化收益']].to_string(index=False))
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()