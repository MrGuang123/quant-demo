"""
风险管理模块
仓位管理、止损止盈等
"""
import pandas as pd
import numpy as np
import config


class RiskManager:
    """
    风险管理器
    """
    
    def __init__(
        self,
        max_position_size: float = config.MAX_POSITION_SIZE,
        stop_loss_pct: float = config.STOP_LOSS_PCT,
        take_profit_pct: float = config.TAKE_PROFIT_PCT
    ):
        """
        初始化风险管理器
        
        Args:
            max_position_size: 最大仓位比例 (0-1)
            stop_loss_pct: 止损百分比
            take_profit_pct: 止盈百分比
        """
        self.max_position_size = max_position_size
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
    
    def calculate_position_size(
        self,
        capital: float,
        entry_price: float,
        risk_per_trade: float = 0.02
    ) -> float:
        """
        计算仓位大小
        
        Args:
            capital: 总资金
            entry_price: 入场价格
            risk_per_trade: 单次交易风险比例 (默认2%)
            
        Returns:
            建议的仓位数量
        """
        # 基于固定风险的仓位计算
        risk_amount = capital * risk_per_trade
        stop_distance = entry_price * self.stop_loss_pct
        
        position_size = risk_amount / stop_distance
        
        # 确保不超过最大仓位
        max_shares = (capital * self.max_position_size) / entry_price
        position_size = min(position_size, max_shares)
        
        return position_size
    
    def calculate_stop_loss(self, entry_price: float, is_long: bool = True) -> float:
        """
        计算止损价格
        
        Args:
            entry_price: 入场价格
            is_long: 是否做多
            
        Returns:
            止损价格
        """
        if is_long:
            return entry_price * (1 - self.stop_loss_pct)
        else:
            return entry_price * (1 + self.stop_loss_pct)
    
    def calculate_take_profit(self, entry_price: float, is_long: bool = True) -> float:
        """
        计算止盈价格
        
        Args:
            entry_price: 入场价格
            is_long: 是否做多
            
        Returns:
            止盈价格
        """
        if is_long:
            return entry_price * (1 + self.take_profit_pct)
        else:
            return entry_price * (1 - self.take_profit_pct)
    
    def apply_stop_loss_take_profit(
        self,
        df: pd.DataFrame,
        entries: pd.Series,
        stop_loss_pct: float = None,
        take_profit_pct: float = None
    ) -> tuple:
        """
        应用止损止盈规则到信号
        
        Args:
            df: 价格数据
            entries: 入场信号
            stop_loss_pct: 止损百分比
            take_profit_pct: 止盈百分比
            
        Returns:
            (修改后的入场信号, 出场信号)
        """
        stop_loss_pct = stop_loss_pct or self.stop_loss_pct
        take_profit_pct = take_profit_pct or self.take_profit_pct
        
        exits = pd.Series(False, index=df.index)
        
        in_position = False
        entry_price = 0
        entry_idx = 0
        
        for i in range(len(df)):
            if entries.iloc[i] and not in_position:
                # 开仓
                in_position = True
                entry_price = df['close'].iloc[i]
                entry_idx = i
            
            elif in_position:
                current_price = df['close'].iloc[i]
                
                # 检查止损
                if current_price <= entry_price * (1 - stop_loss_pct):
                    exits.iloc[i] = True
                    in_position = False
                
                # 检查止盈
                elif current_price >= entry_price * (1 + take_profit_pct):
                    exits.iloc[i] = True
                    in_position = False
        
        return entries, exits
    
    def calculate_kelly_criterion(
        self,
        win_rate: float,
        avg_win: float,
        avg_loss: float
    ) -> float:
        """
        计算凯利公式建议的仓位比例
        
        Args:
            win_rate: 胜率
            avg_win: 平均盈利
            avg_loss: 平均亏损（正数）
            
        Returns:
            建议的仓位比例 (0-1)
        """
        if avg_loss == 0:
            return 0
        
        win_loss_ratio = avg_win / abs(avg_loss)
        kelly = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
        
        # 通常使用Half Kelly或Quarter Kelly更保守
        kelly = max(0, min(kelly * 0.5, self.max_position_size))
        
        return kelly
    
    def check_risk_limits(
        self,
        portfolio_value: float,
        max_drawdown: float,
        consecutive_losses: int,
        max_dd_limit: float = 0.20,
        max_consecutive_losses: int = 5
    ) -> dict:
        """
        检查风险限制
        
        Returns:
            风险检查结果字典
        """
        warnings = []
        
        if max_drawdown > max_dd_limit:
            warnings.append(f"⚠️  回撤过大: {max_drawdown:.2%} (限制: {max_dd_limit:.2%})")
        
        if consecutive_losses >= max_consecutive_losses:
            warnings.append(f"⚠️  连续亏损次数过多: {consecutive_losses} (限制: {max_consecutive_losses})")
        
        return {
            'risk_ok': len(warnings) == 0,
            'warnings': warnings
        }


# ==================== 使用示例 ====================
if __name__ == "__main__":
    # 创建风险管理器
    rm = RiskManager(
        max_position_size=0.95,
        stop_loss_pct=0.02,
        take_profit_pct=0.04
    )
    
    # 计算仓位
    capital = 10000
    entry_price = 50000
    position_size = rm.calculate_position_size(capital, entry_price)
    print(f"建议仓位: {position_size:.4f} BTC")
    print(f"总价值: ${position_size * entry_price:.2f}")
    
    # 计算止损止盈
    stop_loss = rm.calculate_stop_loss(entry_price)
    take_profit = rm.calculate_take_profit(entry_price)
    print(f"\n入场价: ${entry_price}")
    print(f"止损价: ${stop_loss:.2f} ({-rm.stop_loss_pct:.2%})")
    print(f"止盈价: ${take_profit:.2f} ({rm.take_profit_pct:.2%})")
    
    # 凯利公式
    kelly = rm.calculate_kelly_criterion(win_rate=0.55, avg_win=0.02, avg_loss=0.01)
    print(f"\n凯利公式建议仓位: {kelly:.2%}")