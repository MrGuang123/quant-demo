#!/usr/bin/env python3
"""
安装测试脚本
验证所有依赖是否正确安装
"""
import sys


def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    print(f"   当前版本: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("   ❌ Python版本过低！需要 Python 3.10+")
        return False
    else:
        print("   ✅ Python版本符合要求")
        return True


def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    dependencies = {
        'ccxt': 'CCXT (交易所API)',
        'pandas': 'Pandas (数据处理)',
        'numpy': 'NumPy (数值计算)',
        'ta': 'TA (技术分析)',
        'vectorbt': 'VectorBT (回测引擎)',
        'matplotlib': 'Matplotlib (可视化)',
        'plotly': 'Plotly (交互式图表)',
        'sklearn': 'Scikit-learn (机器学习)',
    }
    
    all_ok = True
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description} - 未安装")
            all_ok = False
    
    return all_ok


def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    from pathlib import Path
    
    required_dirs = [
        'data',
        'strategies',
        'backtest',
        'utils',
        'examples'
    ]
    
    required_files = [
        'config.py',
        'requirements.txt',
        'README.md',
        'main.py'
    ]
    
    all_ok = True
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"   ✅ {dir_name}/ 目录")
        else:
            print(f"   ❌ {dir_name}/ 目录缺失")
            all_ok = False
    
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} 缺失")
            all_ok = False
    
    return all_ok


def test_data_fetcher():
    """测试数据获取功能"""
    print("\n🌐 测试数据获取...")
    
    try:
        from data.fetcher import DataFetcher
        
        # fetcher = DataFetcher("binance")
        # fetcher = DataFetcher("okx")
        fetcher = DataFetcher("coinbase")
        print("   ✅ 数据获取器初始化成功")
        
        # 尝试获取少量数据
        print("   🔄 获取测试数据（10根K线）...")
        df = fetcher.fetch_ohlcv("BTC/USDT", "1h", 10, use_cache=False)
        
        if len(df) > 0:
            print(f"   ✅ 成功获取 {len(df)} 根K线")
            print(f"   📊 最新价格: ${df['close'].iloc[-1]:,.2f}")
            return True
        else:
            print("   ❌ 数据为空")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False


def test_strategy():
    """测试策略功能"""
    print("\n📈 测试策略模块...")
    
    try:
        from strategies.ema_cross import EMACrossStrategy
        
        strategy = EMACrossStrategy(20, 60)
        print(f"   ✅ 策略创建成功: {strategy}")
        return True
        
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False


def test_backtest():
    """测试回测引擎"""
    print("\n🔬 测试回测引擎...")
    
    try:
        from backtest.engine import BacktestEngine
        
        engine = BacktestEngine(initial_capital=10000, fees=0.0004)
        print("   ✅ 回测引擎初始化成功")
        return True
        
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("="*60)
    print("🧪 量化交易系统 - 安装测试")
    print("="*60)
    
    results = []
    
    # 运行所有测试
    results.append(("Python版本", check_python_version()))
    results.append(("依赖包", check_dependencies()))
    results.append(("项目结构", check_project_structure()))
    results.append(("数据获取", test_data_fetcher()))
    results.append(("策略模块", test_strategy()))
    results.append(("回测引擎", test_backtest()))
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:15} {status}")
    
    print("="*60)
    print(f"总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已就绪！")
        print("\n下一步:")
        print("  1. 运行示例: python examples/simple_backtest.py")
        print("  2. 阅读文档: 查看 README.md")
        print("  3. 快速开始: 查看 QUICKSTART.md")
    else:
        print("\n⚠️  部分测试失败，请检查安装")
        print("\n解决方案:")
        print("  1. 确保虚拟环境已激活: source .venv/bin/activate")
        print("  2. 重新安装依赖: pip install -r requirements.txt")
        print("  3. 检查网络连接")
        print("  4. 查看错误信息并搜索解决方案")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
