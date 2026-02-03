"""
可视化工具
用于绘制K线图、指标图、回测结果等
"""
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class Visualizer:
    """
    可视化工具类
    """
    
    @staticmethod
    def plot_candlestick(
        df: pd.DataFrame,
        title: str = "K线图",
        show_volume: bool = True,
        signals: dict = None
    ):
        """
        绘制K线图（使用plotly，交互式）
        
        Args:
            df: 包含OHLCV数据的DataFrame
            title: 图表标题
            show_volume: 是否显示成交量
            signals: 交易信号字典 {'entries': Series, 'exits': Series}
        """
        # 创建子图
        if show_volume:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=(title, '成交量')
            )
        else:
            fig = make_subplots(rows=1, cols=1, subplot_titles=(title,))
        
        # K线图
        fig.add_trace(
            go.Candlestick(
                x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='K线'
            ),
            row=1, col=1
        )
        
        # 添加交易信号
        if signals is not None:
            entries = signals.get('entries')
            exits = signals.get('exits')
            
            if entries is not None and entries.sum() > 0:
                buy_points = df[entries]
                fig.add_trace(
                    go.Scatter(
                        x=buy_points['timestamp'],
                        y=buy_points['low'] * 0.98,
                        mode='markers',
                        marker=dict(symbol='triangle-up', size=15, color='green'),
                        name='买入信号'
                    ),
                    row=1, col=1
                )
            
            if exits is not None and exits.sum() > 0:
                sell_points = df[exits]
                fig.add_trace(
                    go.Scatter(
                        x=sell_points['timestamp'],
                        y=sell_points['high'] * 1.02,
                        mode='markers',
                        marker=dict(symbol='triangle-down', size=15, color='red'),
                        name='卖出信号'
                    ),
                    row=1, col=1
                )
        
        # 成交量
        if show_volume:
            colors = ['red' if close < open else 'green' 
                     for close, open in zip(df['close'], df['open'])]
            
            fig.add_trace(
                go.Bar(
                    x=df['timestamp'],
                    y=df['volume'],
                    marker_color=colors,
                    name='成交量',
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # 更新布局
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=800 if show_volume else 600,
            hovermode='x unified'
        )
        
        fig.show()
    
    @staticmethod
    def plot_strategy_signals(
        df: pd.DataFrame,
        entries: pd.Series,
        exits: pd.Series,
        indicators: dict = None,
        title: str = "策略信号"
    ):
        """
        绘制策略信号和指标
        
        Args:
            df: 价格数据
            entries: 买入信号
            exits: 卖出信号
            indicators: 要显示的指标字典 {'name': column_name}
            title: 图表标题
        """
        fig = make_subplots(
            rows=2 if indicators else 1,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.7, 0.3] if indicators else [1]
        )
        
        # 价格线
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['close'],
                mode='lines',
                name='收盘价',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        # 添加指标线（如均线）
        if indicators:
            colors = ['orange', 'purple', 'brown', 'pink']
            for i, (name, col) in enumerate(indicators.items()):
                if col in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=df[col],
                            mode='lines',
                            name=name,
                            line=dict(color=colors[i % len(colors)])
                        ),
                        row=1, col=1
                    )
        
        # 买入信号
        if entries.sum() > 0:
            buy_points = df[entries]
            fig.add_trace(
                go.Scatter(
                    x=buy_points['timestamp'],
                    y=buy_points['close'],
                    mode='markers',
                    marker=dict(symbol='triangle-up', size=12, color='green'),
                    name='买入'
                ),
                row=1, col=1
            )
        
        # 卖出信号
        if exits.sum() > 0:
            sell_points = df[exits]
            fig.add_trace(
                go.Scatter(
                    x=sell_points['timestamp'],
                    y=sell_points['close'],
                    mode='markers',
                    marker=dict(symbol='triangle-down', size=12, color='red'),
                    name='卖出'
                ),
                row=1, col=1
            )
        
        fig.update_layout(
            title=title,
            xaxis_rangeslider_visible=False,
            height=700,
            hovermode='x unified'
        )
        
        fig.show()
    
    @staticmethod
    def plot_backtest_results(portfolio, df: pd.DataFrame):
        """
        绘制回测结果
        包括权益曲线和回撤
        """
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('价格', '权益曲线', '回撤'),
            row_heights=[0.4, 0.3, 0.3]
        )
        
        # 1. 价格
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['close'],
                mode='lines',
                name='价格',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        # 2. 权益曲线
        equity = portfolio.value()
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=equity,
                mode='lines',
                name='权益',
                line=dict(color='green'),
                fill='tozeroy'
            ),
            row=2, col=1
        )
        
        # 3. 回撤
        drawdown = portfolio.drawdown() * 100  # 转换为百分比
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=drawdown,
                mode='lines',
                name='回撤 (%)',
                line=dict(color='red'),
                fill='tozeroy'
            ),
            row=3, col=1
        )
        
        fig.update_layout(
            height=900,
            hovermode='x unified',
            showlegend=True
        )
        
        fig.update_yaxes(title_text="价格", row=1, col=1)
        fig.update_yaxes(title_text="权益", row=2, col=1)
        fig.update_yaxes(title_text="回撤 (%)", row=3, col=1)
        
        fig.show()
    
    @staticmethod
    def plot_multiple_strategies(results_df: pd.DataFrame):
        """
        对比多个策略的表现
        
        Args:
            results_df: 策略对比结果DataFrame
        """
        import plotly.express as px
        
        # 提取数值（去掉百分号等格式）
        df = results_df.copy()
        
        # 创建子图
        metrics = ['总收益率', '夏普比率', '最大回撤', '胜率']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=metrics
        )
        
        # 这里需要根据实际数据格式调整
        # 简化版本：使用柱状图
        print("\n策略对比可视化（简化版）:")
        print(results_df)
    
    @staticmethod
    def plot_parameter_optimization(results_df: pd.DataFrame, param1: str, param2: str):
        """
        绘制参数优化热力图
        
        Args:
            results_df: 优化结果DataFrame
            param1: 第一个参数名
            param2: 第二个参数名
        """
        # 透视表
        pivot_table = results_df.pivot_table(
            values='sharpe_ratio',
            index=param1,
            columns=param2
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='RdYlGn',
            text=pivot_table.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='参数优化热力图（夏普比率）',
            xaxis_title=param2,
            yaxis_title=param1,
            height=600
        )
        
        fig.show()


# ==================== 使用示例 ====================
if __name__ == "__main__":
    from data.fetcher import DataFetcher
    from strategies.ema_cross import EMACrossStrategy
    
    # 获取数据
    fetcher = DataFetcher()
    df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 500)
    
    # 生成信号
    strategy = EMACrossStrategy()
    entries, exits = strategy.generate_signals(df)
    
    # 可视化
    viz = Visualizer()
    
    # K线图with信号
    viz.plot_candlestick(
        df,
        title="BTC/USDT K线图",
        signals={'entries': entries, 'exits': exits}
    )