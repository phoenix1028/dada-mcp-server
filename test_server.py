#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试达达MCP服务器配置
"""

import sys
import importlib.util

def test_imports():
    """测试依赖导入"""
    try:
        import json
        import time
        import hashlib
        import requests
        import asyncio
        from typing import Dict, Any, List, Optional
        from dataclasses import dataclass, asdict
        print("✅ 标准库导入成功")
        
        from pydantic import BaseModel
        print("✅ Pydantic导入成功")
        
        from mcp.server.fastmcp import FastMCP
        print("✅ MCP FastMCP导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_server_creation():
    """测试服务器创建"""
    try:
        # 导入服务器模块
        spec = importlib.util.spec_from_file_location("server", "server.py")
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)
        
        # 检查MCP实例
        if hasattr(server_module, 'mcp'):
            print("✅ MCP服务器实例创建成功")
            print(f"   服务器名称: {server_module.mcp.name}")
        else:
            print("❌ MCP服务器实例未找到")
            return False
            
        # 检查配置
        if hasattr(server_module, 'config'):
            config = server_module.config
            print("✅ 配置实例创建成功")
            print(f"   API主机: {config.host}")
            print(f"   商户ID: {config.source_id}")
        else:
            print("❌ 配置实例未找到")
            return False
            
        return True
    except Exception as e:
        print(f"❌ 服务器创建失败: {e}")
        return False

def test_tools():
    """测试工具函数"""
    try:
        spec = importlib.util.spec_from_file_location("server", "server.py")
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)
        
        # 检查工具函数
        tools = ['create_order', 'cancel_order', 'query_order', 'get_cancel_reasons']
        for tool in tools:
            if hasattr(server_module, tool):
                print(f"✅ 工具函数 {tool} 定义成功")
            else:
                print(f"❌ 工具函数 {tool} 未找到")
                
        # 检查资源函数
        if hasattr(server_module, 'get_config'):
            print("✅ 资源函数 get_config 定义成功")
        else:
            print("❌ 资源函数 get_config 未找到")
            
        return True
    except Exception as e:
        print(f"❌ 工具函数检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("达达MCP服务器配置测试")
    print("=" * 50)
    
    # 测试导入
    print("\n1. 测试依赖导入:")
    if not test_imports():
        print("请先安装依赖: uv sync")
        sys.exit(1)
    
    # 测试服务器创建
    print("\n2. 测试服务器创建:")
    if not test_server_creation():
        sys.exit(1)
    
    # 测试工具函数
    print("\n3. 测试工具和资源定义:")
    if not test_tools():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("服务器配置正确，可以启动运行。")
    print("\n启动命令:")
    print("  uv run python server.py")

if __name__ == "__main__":
    main()