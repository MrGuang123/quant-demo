"""
回测引擎
负责执行策略回测和生成回测报告
"""
import pandas as pd
import numpy as np
import vectorbt as vbt
from typing import Optional, Dict, Any
from strategies.base import BaseStrategy
from .metrics import PerformanceMetrics
import config


class BacktestEngine:
    """
    回测引擎
    
    使用vectorbt进行快速回测
    """
    
    def __init__(
        self,
        initial_capital: float = config.INITIAL_CAPITAL,
        fees: float = config.TRADING_FEE,
        slippage: float = config.SLIPPAGE
    ):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            fees: 交易手续费（百分比，如0.001表示0.1%）
            slippage: 滑点（百分比）
        """
        self.initial_capital = initial_capital
        self.fees = fees
        self.slippage = slippage
        self.portfolio = None
        self.results = {}
    
    def run(
        self,
        df: pd.DataFrame,
        strategy: BaseStrategy,
        price_col: str = 'close'
    ) -> Dict[str, Any]:
        """
        运行回测
        
        Args:
            df: 包含价格数据的DataFrame
            strategy: 交易策略对象
            price_col: 价格列名
            
        Returns:
            回测结果字典
        """
        print(f"\n{'='*60}")
        print(f"🚀 开始回测: {strategy.name}")
        print(f"{'='*60}")
        
        # 生成交易信号
        entries, exits = strategy.generate_signals(df)
        
        # 使用vectorbt进行回测
        self.portfolio = vbt.Portfolio.from_signals(
            close=df[price_col],
            entries=entries,
            exits=exits,
            init_cash=self.initial_capital,
            fees=self.fees,
            slippage=self.slippage,
            freq='1H'  # 假设是1小时数据，根据实际调整
        )
        
        # 计算性能指标
        metrics = PerformanceMetrics(self.portfolio, df)
        results = metrics.calculate_all()
        
        # 添加策略信息
        results['strategy_name'] = strategy.name
        results['strategy_params'] = strategy.get_params()
        results['initial_capital'] = self.initial_capital
        results['fees'] = self.fees
        
        # 添加交易统计
        results['total_signals'] = {
            'entries': int(entries.sum()),
            'exits': int(exits.sum())
        }
        
        self.results = results
        
        # 打印结果
        self._print_results()
        
        return results
    
    def run_multiple_strategies(
        self,
        df: pd.DataFrame,
        strategies: list,
        price_col: str = 'close'
    ) -> pd.DataFrame:
        """
        运行多个策略的回测并对比
        
        Args:
            df: 价格数据
            strategies: 策略列表
            price_col: 价格列名
            
        Returns:
            对比结果DataFrame
        """
        results_list = []
        
        for strategy in strategies:
            result = self.run(df, strategy, price_col)
            results_list.append({
                '策略名称': result['strategy_name'],
                '总收益率': f"{result['total_return']:.2%}",
                '年化收益': f"{result['annual_return']:.2%}",
                '夏普比率': f"{result['sharpe_ratio']:.2f}",
                '最大回撤': f"{result['max_drawdown']:.2%}",
                '胜率': f"{result['win_rate']:.2%}",
                '交易次数': result['total_trades'],
                '盈亏比': f"{result['profit_factor']:.2f}"
            })
        
        comparison_df = pd.DataFrame(results_list)
        
        print(f"\n{'='*80}")
        print("📊 策略对比结果")
        print(f"{'='*80}")
        print(comparison_df.to_string(index=False))
        
        return comparison_df
    
    def optimize_parameters(
        self,
        df: pd.DataFrame,
        strategy_class,
        param_ranges: Dict[str, list],
        price_col: str = 'close'
    ):
        """
        参数优化
        
        Args:
            df: 价格数据
            strategy_class: 策略类
            param_ranges: 参数范围字典，如 {'fast_window': [10, 20, 30], 'slow_window': [50, 60, 70]}
            price_col: 价格列名
            
        Returns:
            最优参数和结果
        """
        print(f"\n{'='*60}")
        print("🔍 开始参数优化...")
        print(f"{'='*60}")
        
        from itertools import product
        
        # 生成所有参数组合
        param_names = list(param_ranges.keys())
        param_values = list(param_ranges.values())
        combinations = list(product(*param_values))
        
        best_sharpe = -np.inf
        best_params = None
        best_result = None
        
        results_list = []
        
        print(f"总共 {len(combinations)} 种参数组合需要测试\n")
        
        for i, combo in enumerate(combinations, 1):
            # 创建参数字典
            params = dict(zip(param_names, combo))
            
            # 创建策略
            strategy = strategy_class(**params)
            
            # 运行回测
            try:
                entries, exits = strategy.generate_signals(df)
                
                portfolio = vbt.Portfolio.from_signals(
                    close=df[price_col],
                    entries=entries,
                    exits=exits,
                    init_cash=self.initial_capital,
                    fees=self.fees
                )
                
                metrics = PerformanceMetrics(portfolio, df)
                result = metrics.calculate_all()
                
                # 记录结果
                result_record = {
                    **params,
                    'sharpe_ratio': result['sharpe_ratio'],
                    'total_return': result['total_return'],
                    'max_drawdown': result['max_drawdown'],
                    'win_rate': result['win_rate']
                }
                results_list.append(result_record)
                
                # 更新最优结果
                if result['sharpe_ratio'] > best_sharpe:
                    best_sharpe = result['sharpe_ratio']
                    best_params = params
                    best_result = result
                
                # 进度提示
                if i % 10 == 0 or i == len(combinations):
                    print(f"进度: {i}/{len(combinations)} - 当前最佳夏普: {best_sharpe:.2f}")
                    
            except Exception as e:
                print(f"参数组合 {params} 失败: {e}")
                continue
        
        # 结果汇总
        results_df = pd.DataFrame(results_list)
        results_df = results_df.sort_values('sharpe_ratio', ascending=False)
        
        print(f"\n{'='*60}")
        print("✅ 优化完成")
        print(f"{'='*60}")
        print(f"最优参数: {best_params}")
        print(f"最优夏普比率: {best_sharpe:.2f}")
        print(f"\nTop 5 参数组合:")
        print(results_df.head().to_string())
        
        return best_params, best_result, results_df
    
    def _print_results(self):
        """打印回测结果"""
        r = self.results
        
        print(f"\n{'='*60}")
        print("📈 回测结果")
        print(f"{'='*60}")
        print(f"策略名称: {r['strategy_name']}")
        print(f"策略参数: {r['strategy_params']}")
        print(f"\n💰 收益指标:")
        print(f"  初始资金: ${r['initial_capital']:,.2f}")
        print(f"  最终资金: ${r['final_value']:,.2f}")
        print(f"  总收益率: {r['total_return']:.2%}")
        print(f"  年化收益: {r['annual_return']:.2%}")
        print(f"\n📊 风险指标:")
        print(f"  最大回撤: {r['max_drawdown']:.2%}")
        print(f"  夏普比率: {r['sharpe_ratio']:.2f}")
        print(f"  波动率: {r['volatility']:.2%}")
        print(f"\n🎯 交易统计:")
        print(f"  总交易次数: {r['total_trades']}")
        print(f"  盈利次数: {r['winning_trades']}")
        print(f"  亏损次数: {r['losing_trades']}")
        print(f"  胜率: {r['win_rate']:.2%}")
        print(f"  盈亏比: {r['profit_factor']:.2f}")
        print(f"  平均盈利: {r['avg_win']:.2%}")
        print(f"  平均亏损: {r['avg_loss']:.2%}")
        print(f"{'='*60}\n")
    
    def get_portfolio(self):
        """获取回测的投资组合对象（用于可视化）"""
        return self.portfolio
    
    def get_results(self):
        """获取回测结果"""
        return self.results


# ==================== 使用示例 ====================
if __name__ == "__main__":
    from data.fetcher import DataFetcher
    from strategies.ema_cross import EMACrossStrategy
    
    # 获取数据
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 1000)
    
    # 创建策略
    strategy = EMACrossStrategy(fast_window=20, slow_window=60)
    
    # 创建回测引擎
    engine = BacktestEngine(
        initial_capital=10000,
        fees=0.0004
    )
    
    # 运行回测
    results = engine.run(df, strategy)