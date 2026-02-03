# ==================== API密钥配置示例 ====================
# 
# 使用方法：
# 1. 复制此文件为 config_local.py
# 2. 在 config_local.py 中填入你的真实API密钥
# 3. config_local.py 已在 .gitignore 中，不会被提交到Git
#
# 注意：config_local.py 会自动覆盖 config.py 中的设置
#

# ==================== 交易所API密钥 ====================

# Binance API（用于实盘交易）
BINANCE_API_KEY = "your_binance_api_key_here"
BINANCE_API_SECRET = "your_binance_api_secret_here"

# OKX API（可选）
OKX_API_KEY = "your_okx_api_key_here"
OKX_API_SECRET = "your_okx_api_secret_here"
OKX_API_PASSWORD = "your_okx_password_here"

# Bybit API（可选）
BYBIT_API_KEY = "your_bybit_api_key_here"
BYBIT_API_SECRET = "your_bybit_api_secret_here"

# ==================== 自定义配置 ====================

# 覆盖默认设置（可选）
# DEFAULT_EXCHANGE = "okx"
# DEFAULT_SYMBOL = "ETH/USDT"
# INITIAL_CAPITAL = 50000
# TRADING_FEE = 0.0002

# ==================== 警告 ====================
# 
# ⚠️  请妥善保管你的API密钥！
# ⚠️  不要将包含真实密钥的文件提交到Git！
# ⚠️  建议只给API密钥授予必要的权限（如只读权限用于回测）
# ⚠️  实盘交易前请务必进行充分测试！
#
