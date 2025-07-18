#!/bin/bash

# 启动达达MCP HTTP Stream服务器 (使用uv)

echo "启动达达配送MCP HTTP Stream服务器..."
echo "使用streamable-http传输协议"
echo ""

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "安装uv包管理器..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 检查是否在uv项目中
if [ ! -f "pyproject.toml" ]; then
    echo "错误: 未找到pyproject.toml文件，请确保在正确的项目目录中运行"
    exit 1
fi

# 使用uv安装依赖
echo "使用uv安装项目依赖..."
uv sync

# 使用uv运行服务器 (streamable-http模式)
echo "启动MCP Streamable HTTP服务器..."
uv run python server.py