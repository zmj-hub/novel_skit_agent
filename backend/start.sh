#!/bin/bash

# 后端服务启动脚本
echo "启动 Novel Skit Agent 后端服务..."

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: Python 3 未安装"
    exit 1
fi

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "错误: requirements.txt 文件不存在"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 启动服务
echo "启动 FastAPI 服务..."
python main.py
