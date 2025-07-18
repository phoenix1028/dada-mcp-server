#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import hashlib
import requests
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP


# Pydantic模型用于结构化响应
class OrderResponse(BaseModel):
    """订单操作响应"""
    status: str
    message: str
    order_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_code: Optional[int] = None


class ConfigInfo(BaseModel):
    """配置信息"""
    host: str
    source_id: str
    shop_no: str
    app_key: str


@dataclass
class Configuration:
    """达达开放平台API接口环境配置"""
    host: str = "http://newopen.qa.imdada.cn"
    callback: str = "http://baidu.com"
    source_id: str = "2079751081"
    shop_no: str = "8f27f5aaae7e48ed"
    app_key: str = "dada0bb505789a2d445"
    app_secret: str = "83a3372d374283c48921bdb98cb47124"


@dataclass
class ProductDetail:
    """产品详情"""
    src_product_no: str
    sku_name: str
    count: float
    unit: str


@dataclass
class OrderDetail:
    """订单详情"""
    shop_no: str
    origin_id: str
    city_code: str
    cargo_price: float
    is_prepay: int
    receiver_name: str
    receiver_address: str
    receiver_lat: float
    receiver_lng: float
    callback: str
    cargo_weight: float
    receiver_phone: str
    tips: float
    info: str
    cargo_type: int
    cargo_num: int
    invoice_title: str
    is_use_insurance: int
    is_finish_code_needed: int
    pick_up_pos: str
    product_list: List[ProductDetail]
    # 发货人信息
    supplier_name: str
    supplier_address: str
    supplier_phone: str
    supplier_lat: float
    supplier_lng: float
    receiver_tel: Optional[str] = None
    origin_mark: Optional[str] = None
    origin_mark_no: Optional[str] = None
    delay_publish_time: Optional[int] = None
    is_direct_delivery: Optional[int] = None


class DaDaAPIClient:
    """达达API客户端基类"""
    
    def __init__(self, config: Configuration = None):
        self.config = config or Configuration()
    
    def _generate_signature(self, data: Dict[str, Any], app_secret: str) -> str:
        """生成签名"""
        sorted_keys = sorted(data.keys())
        sign_str = "".join(f"{key}{data[key]}" for key in sorted_keys)
        final_sign_str = f"{app_secret}{sign_str}{app_secret}"
        md5_hash = hashlib.md5(final_sign_str.encode('utf-8')).hexdigest()
        return md5_hash.upper()
    
    async def _do_invoke_async(self, url: str, params: Dict[str, Any]) -> str:
        """异步执行HTTP请求"""
        import aiohttp
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return await response.text()
    
    def _process_response(self, response_text: str) -> Dict[str, Any]:
        """处理响应结果"""
        try:
            response_data = json.loads(response_text)
            return response_data
        except json.JSONDecodeError:
            return {"status": "fail", "msg": "响应解析失败"}
        except Exception as e:
            return {"status": "fail", "msg": str(e)}


class AddOrderClient(DaDaAPIClient):
    """达达配送新增订单客户端"""
    
    def __init__(self, config: Configuration = None):
        super().__init__(config)
        self.url = f"{self.config.host}/api/order/addOrder"
    
    async def execute_async(self, receiver_name: str, receiver_address: str, receiver_phone: str,
                           receiver_lat: float, receiver_lng: float, supplier_name: str,
                           supplier_address: str, supplier_phone: str, supplier_lat: float,
                           supplier_lng: float, cargo_price: float = 50.0,
                           tips: float = 1.0, info: str = "备注信息") -> Dict[str, Any]:
        """异步执行订单创建"""
        origin_id = f"originId-{int(time.time() * 1000)}"
        
        order_detail = self._build_order_detail(
            origin_id, receiver_name, receiver_address, receiver_phone,
            receiver_lat, receiver_lng, supplier_name, supplier_address,
            supplier_phone, supplier_lat, supplier_lng, cargo_price, tips, info
        )
        
        params = self._generate_params(order_detail)
        
        try:
            response_text = await self._do_invoke_async(self.url, params)
            result = self._process_response(response_text)
            
            if result.get("status") == "success":
                result["order_id"] = origin_id
            
            return result
            
        except Exception as e:
            return {"status": "fail", "msg": str(e), "order_id": origin_id}
    
    def _build_order_detail(self, order_no: str, receiver_name: str, receiver_address: str,
                           receiver_phone: str, receiver_lat: float, receiver_lng: float,
                           supplier_name: str, supplier_address: str, supplier_phone: str,
                           supplier_lat: float, supplier_lng: float, cargo_price: float,
                           tips: float, info: str) -> OrderDetail:
        """构建订单详情"""
        product_detail = ProductDetail(
            src_product_no="xxx",
            sku_name="高原风干牛肉干（麻辣味）250克/袋 | 250克",
            count=2.0,
            unit="件"
        )
        
        return OrderDetail(
            shop_no=self.config.shop_no,
            origin_id=order_no,
            city_code="021",
            cargo_price=cargo_price,
            cargo_num=1,
            tips=tips,
            info=info,
            cargo_weight=3.2,
            is_use_insurance=0,
            is_prepay=0,
            is_finish_code_needed=0,
            cargo_type=50,
            invoice_title="invoiceTitle",
            receiver_name=receiver_name,
            receiver_address=receiver_address,
            receiver_phone=receiver_phone,
            receiver_lat=receiver_lat,
            receiver_lng=receiver_lng,
            callback=self.config.callback,
            pick_up_pos="1号货架",
            product_list=[product_detail],
            # 发货人信息
            supplier_name=supplier_name,
            supplier_address=supplier_address,
            supplier_phone=supplier_phone,
            supplier_lat=supplier_lat,
            supplier_lng=supplier_lng
        )
    
    def _generate_params(self, body: OrderDetail) -> Dict[str, Any]:
        """生成API请求参数"""
        data = {
            "source_id": self.config.source_id,
            "app_key": self.config.app_key,
            "timestamp": int(time.time()),
            "format": "json",
            "v": "1.0",
            "body": json.dumps(asdict(body), ensure_ascii=False)
        }
        
        data["signature"] = self._generate_signature(data, self.config.app_secret)
        return data


class CancelOrderClient(DaDaAPIClient):
    """达达配送取消订单客户端"""
    
    CANCEL_REASONS = {
        1: "没有配送员接单",
        2: "配送员没来取货",
        3: "配送员态度太差",
        4: "顾客取消订单",
        5: "订单填写错误",
        34: "配送员让我取消此单",
        35: "配送员不愿上门取货",
        36: "我不需要配送了",
        37: "配送员以各种理由表示无法完成订单",
        10000: "其他"
    }
    
    def __init__(self, config: Configuration = None):
        super().__init__(config)
        self.url = f"{self.config.host}/api/order/formalCancel"
    
    async def execute_async(self, order_id: str, cancel_reason_id: int = 1, cancel_reason: str = None) -> Dict[str, Any]:
        """异步执行订单取消"""
        params = self._generate_params(order_id, cancel_reason_id, cancel_reason)
        
        try:
            response_text = await self._do_invoke_async(self.url, params)
            return self._process_response(response_text)
            
        except Exception as e:
            return {"status": "fail", "msg": str(e)}
    
    def _generate_params(self, order_id: str, cancel_reason_id: int, cancel_reason: str = None) -> Dict[str, Any]:
        """生成API请求参数"""
        body = {
            "order_id": order_id,
            "cancel_reason_id": cancel_reason_id
        }
        
        if cancel_reason_id == 10000 and cancel_reason:
            body["cancel_reason"] = cancel_reason
        elif cancel_reason:
            body["cancel_reason"] = cancel_reason
        
        data = {
            "source_id": self.config.source_id,
            "app_key": self.config.app_key,
            "timestamp": int(time.time()),
            "format": "json",
            "v": "1.0",
            "body": json.dumps(body, ensure_ascii=False)
        }
        
        data["signature"] = self._generate_signature(data, self.config.app_secret)
        return data


class QueryOrderClient(DaDaAPIClient):
    """达达配送查询订单客户端"""
    
    def __init__(self, config: Configuration = None):
        super().__init__(config)
        self.url = f"{self.config.host}/api/order/status/query"
    
    async def execute_async(self, order_id: str) -> Dict[str, Any]:
        """异步执行订单查询"""
        params = self._generate_params(order_id)
        
        try:
            response_text = await self._do_invoke_async(self.url, params)
            return self._process_response(response_text)
            
        except Exception as e:
            return {"status": "fail", "msg": str(e)}
    
    def _generate_params(self, order_id: str) -> Dict[str, Any]:
        """生成API请求参数"""
        body = {"order_id": order_id}
        
        data = {
            "source_id": self.config.source_id,
            "app_key": self.config.app_key,
            "timestamp": int(time.time()),
            "format": "json",
            "v": "1.0",
            "body": json.dumps(body, ensure_ascii=False)
        }
        
        data["signature"] = self._generate_signature(data, self.config.app_secret)
        return data


# 创建MCP服务器实例
mcp = FastMCP("DaDa Delivery Service")

# 全局配置实例
config = Configuration()


@mcp.tool()
async def create_order(
    receiver_name: str,
    receiver_address: str,
    receiver_phone: str,
    receiver_lat: float,
    receiver_lng: float,
    supplier_name: str,
    supplier_address: str,
    supplier_phone: str,
    supplier_lat: float,
    supplier_lng: float,
    cargo_price: float = 50.0,
    tips: float = 0.0,
    info: str = "备注信息"
) -> OrderResponse:
    """创建达达配送订单
    
    Args:
        receiver_name: 收货人姓名
        receiver_address: 收货地址
        receiver_phone: 收货人电话
        receiver_lat: 收货地址纬度
        receiver_lng: 收货地址经度
        supplier_name: 发货人姓名
        supplier_address: 发货人地址
        supplier_phone: 发货人电话
        supplier_lat: 发货人地址纬度
        supplier_lng: 发货人地址经度
        cargo_price: 商品价格（默认50.0）
        tips: 小费（默认0.0）
        info: 备注信息（默认"备注信息"）
    
    Returns:
        订单创建结果
    """
    client = AddOrderClient(config)
    result = await client.execute_async(
        receiver_name, receiver_address, receiver_phone,
        receiver_lat, receiver_lng, supplier_name, supplier_address, 
        supplier_phone, supplier_lat, supplier_lng, cargo_price, tips, info
    )
    
    if result.get("status") == "success":
        return OrderResponse(
            status="success",
            message="订单创建成功",
            order_id=result.get("order_id"),
            result=result.get("result")
        )
    else:
        return OrderResponse(
            status="error",
            message=result.get("msg", "订单创建失败"),
            error_code=result.get("code")
        )


@mcp.tool()
async def cancel_order(
    order_id: str,
    cancel_reason_id: int = 1,
    cancel_reason: str = None
) -> OrderResponse:
    """取消达达配送订单
    
    Args:
        order_id: 订单ID
        cancel_reason_id: 取消原因ID（1-没有配送员接单, 2-配送员没来取货, 3-配送员态度太差, 4-顾客取消订单, 5-订单填写错误, 10000-其他）
        cancel_reason: 自定义取消原因（当cancel_reason_id为10000时必填）
    
    Returns:
        订单取消结果
    """
    client = CancelOrderClient(config)
    result = await client.execute_async(order_id, cancel_reason_id, cancel_reason)
    
    if result.get("status") == "success":
        return OrderResponse(
            status="success",
            message="订单取消成功",
            order_id=order_id,
            result=result.get("result")
        )
    else:
        return OrderResponse(
            status="error",
            message=result.get("msg", "订单取消失败"),
            order_id=order_id,
            error_code=result.get("code")
        )


@mcp.tool()
async def query_order(order_id: str) -> OrderResponse:
    """查询达达配送订单状态
    
    Args:
        order_id: 订单ID
    
    Returns:
        订单状态查询结果
    """
    client = QueryOrderClient(config)
    result = await client.execute_async(order_id)
    
    if result.get("status") == "success":
        return OrderResponse(
            status="success",
            message="订单查询成功",
            order_id=order_id,
            result=result.get("result")
        )
    else:
        return OrderResponse(
            status="error",
            message=result.get("msg", "订单查询失败"),
            order_id=order_id,
            error_code=result.get("code")
        )


@mcp.tool()
def get_cancel_reasons() -> Dict[int, str]:
    """获取可用的取消原因列表
    
    Returns:
        取消原因ID到描述的映射
    """
    return CancelOrderClient.CANCEL_REASONS


# 添加资源支持
@mcp.resource("dada://config")
async def get_config() -> ConfigInfo:
    """获取达达配送配置信息"""
    return ConfigInfo(
        host=config.host,
        source_id=config.source_id,
        shop_no=config.shop_no,
        app_key=config.app_key
    )


# Run server with streamable-http transport
if __name__ == "__main__":
    print("启动达达配送MCP服务器 (HTTP Stream模式)")
    print("可用的工具:")
    print("1. create_order - 创建配送订单")
    print("2. cancel_order - 取消配送订单")
    print("3. query_order - 查询订单状态")
    print("4. get_cancel_reasons - 获取取消原因列表")
    print("\n可用的资源:")
    print("1. dada://config - 获取配置信息")
    print("\n正在启动服务器...")
    
    # 使用streamable-http传输 (推荐的HTTP Stream方式)
    mcp.run(transport="streamable-http")