@echo off

:: 后端服务启动脚本
echo 启动 Novel Skit Agent 后端服务...

:: 检查 Python 环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Python 未安装
    pause
    exit /b 1
)

:: 检查依赖
if not exist "requirements.txt" (
    echo 错误: requirements.txt 文件不存在
    pause
    exit /b 1
)

:: 安装依赖
echo 安装依赖...
pip install -r requirements.txt

:: 启动服务
echo 启动 FastAPI 服务...
python main.py
pause
