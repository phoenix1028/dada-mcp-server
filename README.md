# 达达跑腿MCP服务器

这是一个达达跑腿mcp服务器，基于最新MCP Python SDK 1.12.0，使用streamable-http传输协议

## 功能特性

- ✅ 创建配送订单 (`create_order`)
- ✅ 取消配送订单 (`cancel_order`) 
- ✅ 查询订单状态 (`query_order`)
- ✅ 获取取消原因列表 (`get_cancel_reasons`)
- ✅ 使用streamable-http传输协议 (生产推荐)
- ✅ 异步API调用
- ✅ 配置资源访问

## 系统要求

- Python 3.10+
- MCP Python SDK 1.12.0+

## 安装

### 方法1: 使用uv (推荐)

```bash
# 如果还没有安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆或进入项目目录
cd dada-mcp-server

# uv会自动根据pyproject.toml安装依赖
uv sync
```

### 方法2: 使用pip

```bash
pip install "mcp>=1.12.0" "requests>=2.31.0" "aiohttp>=3.8.0" "uvicorn>=0.24.0"
```

## 运行方式

### Streamable HTTP模式 (生产推荐)

```bash
# 使用uv直接运行
uv run python server.py

# 或使用启动脚本
./start_http_server.sh
```

## 使用uv的完整工作流程

```bash
# 1. 安装uv (如果未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 进入项目目录
cd dada-mcp-server

# 3. 同步依赖
uv sync

# 4. 运行MCP服务器 (streamable-http传输)
uv run python server.py

# 5. 运行任何MCP相关命令
uv run mcp --help
```

## MCP工具说明

### 1. create_order - 创建配送订单

创建一个新的达达配送订单。

**参数:**
- `receiver_name` (str): 收货人姓名
- `receiver_address` (str): 收货地址  
- `receiver_phone` (str): 收货人电话
- `receiver_lat` (float): 收货地址纬度
- `receiver_lng` (float): 收货地址经度
- `cargo_price` (float, 可选): 商品价格，默认50.0
- `tips` (float, 可选): 小费，默认1.0
- `info` (str, 可选): 备注信息，默认"备注信息"

**返回:** JSON格式的订单创建结果，包含订单ID

### 2. cancel_order - 取消配送订单

取消一个已创建的配送订单。

**参数:**
- `order_id` (str): 订单ID
- `cancel_reason_id` (int, 可选): 取消原因ID，默认1
- `cancel_reason` (str, 可选): 自定义取消原因

**取消原因ID说明:**
- 1: 没有配送员接单
- 2: 配送员没来取货
- 3: 配送员态度太差
- 4: 顾客取消订单
- 5: 订单填写错误
- 10000: 其他（需要提供cancel_reason）

### 3. query_order - 查询订单状态

查询指定订单的当前状态。

**参数:**
- `order_id` (str): 订单ID

**返回:** JSON格式的订单状态信息

### 4. get_cancel_reasons - 获取取消原因列表

获取所有可用的订单取消原因。

**返回:** JSON格式的取消原因映射表

## MCP资源

### dada://config - 配置信息

访问达达配送服务的配置信息（不包含敏感数据）。

## MCP客户端连接

### FastGPT集成

服务器启动后，MCP客户端（如FastGPT）可以通过streamable-http协议连接：

```bash
# 服务器启动后会显示监听地址和端口
# 例如: http://localhost:8080
# 将此地址配置到FastGPT的MCP服务器设置中
```

## 开发和调试

启动服务器进行开发调试：

```bash
uv run python server.py
```

服务器将使用streamable-http传输协议运行，支持现代MCP over HTTP连接。

## uv项目管理

```bash
# 添加新依赖
uv add package-name

# 移除依赖  
uv remove package-name

# 更新依赖
uv sync --upgrade

# 检查项目状态
uv tree
```

## 版本信息

- MCP Python SDK: >=1.12.0
- 传输协议: streamable-http (生产推荐)
- Python要求: >=3.10
- 包管理器: uv (推荐)

## 许可证

MIT License
