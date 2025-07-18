#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安装MCP服务器依赖的脚本
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--break-system-packages", "--user", package
        ])
        print(f"✅ 成功安装: {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {package} - {e}")
        return False

def main():
    """主安装函数"""
    print("达达MCP服务器依赖安装")
    print("=" * 50)
    
    # 需要安装的包
    packages = [
        "mcp>=1.12.0",
        "requests>=2.31.0", 
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0"
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"\n正在安装: {package}")
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"安装完成: {success_count}/{len(packages)} 个包安装成功")
    
    if success_count == len(packages):
        print("✅ 所有依赖安装成功！")
        print("\n现在可以运行服务器:")
        print("  python3 server.py")
    else:
        print("❌ 部分依赖安装失败")
        sys.exit(1)

if __name__ == "__main__":
    main()