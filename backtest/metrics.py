"""
性能指标计算模块
计算各种回测性能指标
"""
import pandas as pd
import numpy as np
from typing import Dict, Any


class PerformanceMetrics:
    """
    性能指标计算器
    """
    
    def __init__(self, portfolio, df: pd.DataFrame):
        """
        初始化
        
        Args:
            portfolio: vectorbt的Portfolio对象
            df: 原始价格数据
        """
        self.portfolio = portfolio
        self.df = df
    
    def calculate_all(self) -> Dict[str, Any]:
        """
        计算所有性能指标
        
        Returns:
            包含所有指标的字典
        """
        metrics = {}
        
        # 基本指标
        metrics['initial_capital'] = self.portfolio.init_cash
        metrics['final_value'] = self.portfolio.final_value
        metrics['total_return'] = self.portfolio.total_return
        metrics['annual_return'] = self.calculate_annual_return()
        
        # 风险指标
        metrics['max_drawdown'] = abs(self.portfolio.max_drawdown)
        metrics['sharpe_ratio'] = self.portfolio.sharpe_ratio
        metrics['sortino_ratio'] = self.calculate_sortino_ratio()
        metrics['volatility'] = self.calculate_volatility()
        metrics['calmar_ratio'] = self.calculate_calmar_ratio()
        
        # 交易统计
        trades = self.portfolio.trades.records_readable
        metrics['total_trades'] = len(trades) if len(trades) > 0 else 0
        
        if len(trades) > 0:
            metrics['winning_trades'] = len(trades[trades['PnL'] > 0])
            metrics['losing_trades'] = len(trades[trades['PnL'] <= 0])
            metrics['win_rate'] = metrics['winning_trades'] / metrics['total_trades'] if metrics['total_trades'] > 0 else 0
            
            winning_pnl = trades[trades['PnL'] > 0]['Return'].values
            losing_pnl = trades[trades['PnL'] <= 0]['Return'].values
            
            metrics['avg_win'] = np.mean(winning_pnl) if len(winning_pnl) > 0 else 0
            metrics['avg_loss'] = np.mean(losing_pnl) if len(losing_pnl) > 0 else 0
            
            total_wins = np.sum(winning_pnl) if len(winning_pnl) > 0 else 0
            total_losses = abs(np.sum(losing_pnl)) if len(losing_pnl) > 0 else 0
            metrics['profit_factor'] = total_wins / total_losses if total_losses != 0 else 0
            
            metrics['avg_trade_duration'] = trades['Duration'].mean()
            metrics['max_consecutive_wins'] = self.calculate_max_consecutive_wins(trades)
            metrics['max_consecutive_losses'] = self.calculate_max_consecutive_losses(trades)
        else:
            metrics['winning_trades'] = 0
            metrics['losing_trades'] = 0
            metrics['win_rate'] = 0
            metrics['avg_win'] = 0
            metrics['avg_loss'] = 0
            metrics['profit_factor'] = 0
            metrics['avg_trade_duration'] = pd.Timedelta(0)
            metrics['max_consecutive_wins'] = 0
            metrics['max_consecutive_losses'] = 0
        
        # 其他指标
        metrics['total_fees'] = self.portfolio.trades.records['Fees'].sum() if len(trades) > 0 else 0
        
        return metrics
    
    def calculate_annual_return(self) -> float:
        """计算年化收益率"""
        try:
            total_return = self.portfolio.total_return
            n_days = (self.df['timestamp'].iloc[-1] - self.df['timestamp'].iloc[0]).days
            n_years = n_days / 365.25
            if n_years > 0:
                annual_return = (1 + total_return) ** (1 / n_years) - 1
                return annual_return
            return 0
        except:
            return 0
    
    def calculate_sortino_ratio(self, risk_free_rate: float = 0.0) -> float:
        """
        计算索提诺比率
        只考虑下行波动率
        """
        try:
            returns = self.portfolio.returns
            excess_returns = returns - risk_free_rate / 252  # 假设252个交易日
            downside_returns = excess_returns[excess_returns < 0]
            
            if len(downside_returns) > 0:
                downside_std = np.sqrt(np.mean(downside_returns ** 2))
                if downside_std != 0:
                    sortino = np.mean(excess_returns) / downside_std * np.sqrt(252)
                    return sortino
            return 0
        except:
            return 0
    
    def calculate_volatility(self) -> float:
        """计算年化波动率"""
        try:
            returns = self.portfolio.returns
            volatility = returns.std() * np.sqrt(252)  # 年化
            return volatility
        except:
            return 0
    
    def calculate_calmar_ratio(self) -> float:
        """
        计算卡玛比率
        年化收益 / 最大回撤
        """
        try:
            annual_return = self.calculate_annual_return()
            max_dd = abs(self.portfolio.max_drawdown)
            if max_dd != 0:
                return annual_return / max_dd
            return 0
        except:
            return 0
    
    def calculate_max_consecutive_wins(self, trades: pd.DataFrame) -> int:
        """计算最大连续盈利次数"""
        if len(trades) == 0:
            return 0
        
        wins = (trades['PnL'] > 0).astype(int)
        max_consecutive = 0
        current_consecutive = 0
        
        for win in wins:
            if win:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def calculate_max_consecutive_losses(self, trades: pd.DataFrame) -> int:
        """计算最大连续亏损次数"""
        if len(trades) == 0:
            return 0
        
        losses = (trades['PnL'] <= 0).astype(int)
        max_consecutive = 0
        current_consecutive = 0
        
        for loss in losses:
            if loss:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def get_equity_curve(self) -> pd.Series:
        """获取权益曲线"""
        return self.portfolio.value()
    
    def get_drawdown_series(self) -> pd.Series:
        """获取回撤序列"""
        return self.portfolio.drawdown()