# 🚀 达达跑腿MCP服务器启动指南

## ✅ 安装状态
- ✅ Python 3.12.3 (满足 >=3.10 要求)
- ✅ MCP Python SDK 1.12.0 已安装
- ✅ 所有依赖已安装
- ✅ 服务器配置测试通过

## 🎯 快速启动

### 启动服务器
```bash
python3 server.py
```

### 服务器信息
- **地址**: http://127.0.0.1:8000
- **协议**: streamable-http
- **状态**: 准备就绪

## 🔧 MCP工具列表

### 1. create_order
创建达达配送订单
```json
{
  "receiver_name": "张三",
  "receiver_address": "上海市浦东新区东方渔人码头",
  "receiver_phone": "18500000000",
  "receiver_lat": 31.257801,
  "receiver_lng": 121.538842,
  "supplier_name": "李四",
  "supplier_address": "上海市浦东新区陆家嘴金融中心",
  "supplier_phone": "18600000000",
  "supplier_lat": 31.235801,
  "supplier_lng": 121.508842,
  "cargo_price": 50.0,
  "tips": 1.0,
  "info": "备注信息"
}
```

### 2. cancel_order
取消配送订单
```json
{
  "order_id": "originId-1234567890",
  "cancel_reason_id": 1
}
```

### 3. query_order
查询订单状态
```json
{
  "order_id": "originId-1234567890"
}
```

### 4. get_cancel_reasons
获取取消原因列表 (无参数)

## 📡 MCP资源

### dada://config
获取服务器配置信息

## 🔗 FastGPT集成

1. **启动MCP服务器**:
   ```bash
   python3 server.py
   ```

2. **记录服务器地址**: 
   `http://127.0.0.1:8000`

3. **在FastGPT中配置**:
   - 添加MCP服务器
   - 输入地址: `http://127.0.0.1:8000`
   - 协议选择: streamable-http

4. **开始使用**:
   - 创建订单
   - 查询订单状态
   - 取消订单
   - 管理配送任务

## 🛠️ 故障排除

### 端口被占用
如果8000端口被占用，服务器会自动选择其他端口，查看启动日志获取实际端口。

### 依赖问题
```bash
python3 install_deps.py
```

### 测试服务器
```bash
python3 test_server.py
```

## 📝 项目文件

- `server.py` - MCP服务器主文件
- `install_deps.py` - 依赖安装脚本
- `test_server.py` - 配置测试脚本
- `pyproject.toml` - 项目配置
- `README.md` - 详细文档

---

**🎉 达达跑腿MCP服务器已准备就绪，可以与FastGPT集成使用！**