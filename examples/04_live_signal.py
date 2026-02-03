"""
示例4: 实时信号监控
监控市场并生成交易信号（模拟实盘）
"""
import sys
sys.path.append('..')

from data.fetcher import DataFetcher
from data.processor import DataProcessor
from strategies.ema_cross import EMACrossStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
import time
from datetime import datetime


class SignalMonitor:
    """信号监控器"""
    
    def __init__(self, strategy, exchange="binance", symbol="BTC/USDT", timeframe="5m"):
        """
        初始化监控器
        
        Args:
            strategy: 交易策略
            exchange: 交易所
            symbol: 交易对
            timeframe: 时间周期
        """
        self.strategy = strategy
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.fetcher = DataFetcher(exchange)
        self.processor = DataProcessor()
        self.last_signal = None
    
    def check_signals(self):
        """检查当前信号"""
        try:
            # 获取最新数据
            df = self.fetcher.fetch_ohlcv(
                symbol=self.symbol,
                timeframe=self.timeframe,
                limit=200,
                use_cache=False  # 不使用缓存，获取最新数据
            )
            
            # 处理数据
            df = self.processor.add_technical_indicators(df)
            df = self.processor.clean_data(df)
            
            # 生成信号
            entries, exits = self.strategy.generate_signals(df)
            
            # 获取最新一根K线的信号
            latest_entry = entries.iloc[-1]
            latest_exit = exits.iloc[-1]
            latest_price = df['close'].iloc[-1]
            latest_time = df['timestamp'].iloc[-1]
            
            # 输出信号
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{current_time}] 检查 {self.symbol} {self.timeframe}")
            print(f"当前价格: ${latest_price:,.2f}")
            
            if latest_entry:
                signal = f"🟢 买入信号 @ ${latest_price:,.2f}"
                if self.last_signal != "BUY":
                    print(f"{'='*60}")
                    print(f"⚡ {signal}")
                    print(f"策略: {self.strategy.name}")
                    print(f"时间: {latest_time}")
                    print(f"{'='*60}")
                    self.last_signal = "BUY"
                    
                    # 这里可以添加实际的交易逻辑
                    # self.place_order("buy", latest_price)
                else:
                    print(f"   持续看多...")
                    
            elif latest_exit:
                signal = f"🔴 卖出信号 @ ${latest_price:,.2f}"
                if self.last_signal != "SELL":
                    print(f"{'='*60}")
                    print(f"⚡ {signal}")
                    print(f"策略: {self.strategy.name}")
                    print(f"时间: {latest_time}")
                    print(f"{'='*60}")
                    self.last_signal = "SELL"
                    
                    # 这里可以添加实际的交易逻辑
                    # self.place_order("sell", latest_price)
                else:
                    print(f"   持续看空...")
            else:
                print(f"   无信号，观望中...")
                self.last_signal = None
            
            return latest_entry, latest_exit, latest_price
            
        except Exception as e:
            print(f"❌ 检查信号时出错: {e}")
            return False, False, 0
    
    def run(self, interval_seconds=60):
        """
        持续运行监控
        
        Args:
            interval_seconds: 检查间隔（秒）
        """
        print("=" * 80)
        print(f"🚀 启动信号监控")
        print("=" * 80)
        print(f"交易对: {self.symbol}")
        print(f"周期: {self.timeframe}")
        print(f"策略: {self.strategy.name}")
        print(f"检查间隔: {interval_seconds} 秒")
        print(f"按 Ctrl+C 停止监控")
        print("=" * 80)
        
        try:
            while True:
                self.check_signals()
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  监控已停止")


def main():
    """主函数"""
    print("=" * 80)
    print("示例4: 实时信号监控")
    print("=" * 80)
    
    # 创建策略
    print("\n选择监控策略:")
    print("1. EMA交叉策略（推荐用于趋势市场）")
    print("2. RSI策略（推荐用于震荡市场）")
    print("3. MACD策略（中期趋势）")
    
    choice = input("\n请选择 (1-3, 默认1): ").strip() or "1"
    
    if choice == "1":
        strategy = EMACrossStrategy(fast_window=20, slow_window=60)
    elif choice == "2":
        strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    elif choice == "3":
        strategy = MACDStrategy()
    else:
        strategy = EMACrossStrategy(fast_window=20, slow_window=60)
    
    # 选择交易对
    print("\n选择交易对:")
    print("1. BTC/USDT")
    print("2. ETH/USDT")
    print("3. 自定义")
    
    symbol_choice = input("\n请选择 (1-3, 默认1): ").strip() or "1"
    
    if symbol_choice == "1":
        symbol = "BTC/USDT"
    elif symbol_choice == "2":
        symbol = "ETH/USDT"
    elif symbol_choice == "3":
        symbol = input("请输入交易对 (如 BNB/USDT): ").strip()
    else:
        symbol = "BTC/USDT"
    
    # 选择时间周期
    print("\n选择时间周期:")
    print("1. 1分钟 (1m)")
    print("2. 5分钟 (5m)")
    print("3. 15分钟 (15m)")
    print("4. 1小时 (1h)")
    
    tf_choice = input("\n请选择 (1-4, 默认2): ").strip() or "2"
    
    timeframes = {"1": "1m", "2": "5m", "3": "15m", "4": "1h"}
    timeframe = timeframes.get(tf_choice, "5m")
    
    # 检查间隔
    intervals = {"1m": 30, "5m": 60, "15m": 180, "1h": 300}
    interval = intervals.get(timeframe, 60)
    
    # 创建监控器
    monitor = SignalMonitor(
        strategy=strategy,
        exchange="binance",
        symbol=symbol,
        timeframe=timeframe
    )
    
    # 先检查一次当前信号
    print("\n🔍 检查当前市场状态...")
    monitor.check_signals()
    
    # 询问是否继续监控
    continue_monitor = input("\n是否开启持续监控？(y/n, 默认n): ").strip().lower()
    
    if continue_monitor == 'y':
        monitor.run(interval_seconds=interval)
    else:
        print("\n✅ 单次检查完成")


if __name__ == "__main__":
    main()