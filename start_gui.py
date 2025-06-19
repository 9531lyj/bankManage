#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行管理系统GUI启动脚本
简化的启动入口，自动检查依赖并启动GUI界面
"""

import sys
import os

def check_dependencies():
    """检查必要的依赖包"""
    required_packages = [
        'mysql.connector',
        'tabulate'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_database_config():
    """检查数据库配置"""
    try:
        from DatabaseConnector import DatabaseConnector
        db = DatabaseConnector()
        if db.connect():
            print("数据库连接测试成功")
            db.close()
            return True
        else:
            print("数据库连接失败，请检查配置")
            return False
    except Exception as e:
        print(f"数据库配置检查失败: {e}")
        print("请确保MySQL服务已启动，并检查DatabaseConnector.py中的连接参数")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("银行管理系统 GUI 启动器")
    print("=" * 50)
    
    # 检查依赖
    print("1. 检查Python依赖包...")
    if not check_dependencies():
        sys.exit(1)
    print("   ✓ 依赖包检查通过")
    
    # 检查数据库连接
    print("2. 检查数据库连接...")
    if not check_database_config():
        print("   ✗ 数据库连接失败")
        print("\n请确保:")
        print("   - MySQL服务已启动")
        print("   - 数据库'银行'已创建")
        print("   - DatabaseConnector.py中的连接参数正确")
        sys.exit(1)
    print("   ✓ 数据库连接正常")
    
    # 启动GUI
    print("3. 启动GUI界面...")
    try:
        from BankSystemGUI import BankSystemGUIComplete
        print("   ✓ GUI模块加载成功")
        print("\n正在启动银行管理系统GUI界面...")
        print("=" * 50)
        
        app = BankSystemGUIComplete()
        app.run()
        
    except ImportError as e:
        print(f"   ✗ GUI模块加载失败: {e}")
        print("请确保BankSystemGUI.py文件存在")
        sys.exit(1)
    except Exception as e:
        print(f"   ✗ GUI启动失败: {e}")
        print("请检查系统配置或查看错误日志")
        sys.exit(1)

if __name__ == "__main__":
    main()
