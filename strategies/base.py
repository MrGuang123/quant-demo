"""
策略基类
所有交易策略都应该继承这个类
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple


class BaseStrategy(ABC):
    """
    策略基类
    
    子类需要实现 generate_signals 方法
    """
    
    def __init__(self, name: str = "BaseStrategy"):
        """
        初始化策略
        
        Args:
            name: 策略名称
        """
        self.name = name
        self.params = {}
    
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        生成交易信号
        
        Args:
            df: 包含价格和指标的DataFrame
            
        Returns:
            (entries, exits) 买入信号和卖出信号的布尔Series
        """
        pass
    
    def set_params(self, **kwargs):
        """设置策略参数"""
        self.params.update(kwargs)
        return self
    
    def get_params(self) -> dict:
        """获取策略参数"""
        return self.params
    
    def __repr__(self):
        params_str = ', '.join([f"{k}={v}" for k, v in self.params.items()])
        return f"{self.name}({params_str})"