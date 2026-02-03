## 初始化环境
### 1. 安装 Python 3.12
brew install python@3.12

### 2. 删除旧虚拟环境
rm -rf .venv

### 3. 创建新虚拟环境
python3.12 -m venv .venv

### 4. 激活环境
source .venv/bin/activate

### 5. 安装依赖
pip install ccxt vectorbt pandas ta matplotlib plotly scikit-learn

## 实际工作流
### 1. 创建项目
mkdir my-quant-project
cd my-quant-project

### 2. 创建虚拟环境
python3.12 -m venv .venv

### 3. 激活环境（每次打开终端都要做）
source .venv/bin/activate
### 现在命令提示符变成：(.venv) user@computer:~/my-quant-project$

### 4. 安装包（只在当前环境）
pip install ccxt pandas vectorbt

### 5. 运行项目
python main.py

### 6. 导出依赖
pip freeze > requirements.txt

### 7. 退出虚拟环境
deactivate

### 8. 完全删除环境（如果需要）
rm -rf .venv