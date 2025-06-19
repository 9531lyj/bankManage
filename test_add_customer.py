#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试添加客户功能
"""

from BankSystem import BankSystem
import traceback

def test_add_customer():
    """测试添加客户功能"""
    try:
        print("正在初始化银行系统...")
        bank = BankSystem()
        print("银行系统初始化成功")
        
        # 测试数据
        test_customers = [
            ("张三", "110101199001011234", "13800000001", "北京市朝阳区"),
            ("李四", "110101199002022345", "13800000002", "上海市浦东区"),
            ("王五", "110101199003033456", "13800000003", None)
        ]
        
        print("\n开始测试添加客户...")
        for i, (name, pid, phone, addr) in enumerate(test_customers, 1):
            print(f"\n测试 {i}: 添加客户 {name}")
            print(f"  身份证: {pid}")
            print(f"  电话: {phone}")
            print(f"  地址: {addr or '无'}")
            
            try:
                result = bank.customer_service.add_customer(name, pid, phone, addr)
                if result:
                    print(f"  ✓ 客户 {name} 添加成功")
                else:
                    print(f"  ✗ 客户 {name} 添加失败")
            except Exception as e:
                print(f"  ✗ 添加客户 {name} 时出错: {e}")
                traceback.print_exc()
        
        # 查询所有客户验证
        print("\n查询所有客户验证结果:")
        customers = bank.customer_service.get_customer_info()
        if customers:
            for customer in customers:
                print(f"  ID: {customer['customerID']}, 姓名: {customer['customerName']}, "
                      f"身份证: {customer['PID']}, 电话: {customer['telephone']}")
        else:
            print("  没有找到客户数据")
        
        bank.close()
        print("\n测试完成")
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_add_customer()
