# 达达跑腿MCP服务器 - 快速开始

## 项目概述

这是一个为FastGPT设计的达达跑腿配送服务MCP服务器，提供创建订单、取消订单、查询订单等功能。

## 快速启动

### 1. 安装依赖

```bash
# 安装uv包管理器 (如果未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入项目目录
cd dada-mcp-server

# 安装项目依赖
uv sync
```

### 2. 启动服务器

```bash
# 方法1: 直接启动
uv run python server.py

# 方法2: 使用脚本启动
./start_http_server.sh
```

### 3. 服务器信息

- **传输协议**: streamable-http
- **默认端口**: 自动分配 (查看控制台输出)
- **API端点**: 服务器启动后显示完整地址

## MCP工具功能

### 1. create_order - 创建配送订单
```
参数:
- receiver_name: 收货人姓名
- receiver_address: 收货地址  
- receiver_phone: 收货人电话
- receiver_lat: 纬度
- receiver_lng: 经度
- cargo_price: 商品价格 (可选)
- tips: 小费 (可选)
- info: 备注 (可选)
```

### 2. cancel_order - 取消订单
```
参数:
- order_id: 订单ID
- cancel_reason_id: 取消原因ID (可选)
- cancel_reason: 自定义原因 (可选)
```

### 3. query_order - 查询订单状态
```
参数:
- order_id: 订单ID
```

### 4. get_cancel_reasons - 获取取消原因列表
```
无参数，返回所有可用的取消原因
```

## 资源

### dada://config - 配置信息
返回服务器配置信息（不包含敏感数据）

## FastGPT集成

1. 启动MCP服务器
2. 记录服务器地址 (如: http://localhost:8080)
3. 在FastGPT中配置MCP服务器地址
4. 开始使用达达配送功能

## 故障排除

### 常见问题

1. **Python版本错误**: 需要Python 3.10+
2. **依赖缺失**: 运行 `uv sync` 安装依赖
3. **端口占用**: 服务器会自动选择可用端口

### 测试服务器

```bash
# 运行配置测试
python test_server.py
```

## 项目结构

```
dada-mcp-server/
├── server.py              # MCP服务器主文件
├── pyproject.toml          # 项目依赖配置
├── start_http_server.sh    # 启动脚本
├── test_server.py          # 测试脚本
├── README.md              # 详细文档
└── QUICKSTART.md          # 快速开始指南
```