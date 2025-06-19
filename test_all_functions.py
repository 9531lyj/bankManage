#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行管理系统全功能测试脚本
"""

from BankSystem import BankSystem
import traceback
from datetime import datetime

def test_customer_service(bank):
    """测试客户服务功能"""
    print("\n" + "="*50)
    print("测试客户服务功能")
    print("="*50)
    
    try:
        # 1. 添加客户
        print("1. 测试添加客户...")
        result = bank.customer_service.add_customer("测试用户", "110101199001010001", "13900000001", "测试地址")
        print(f"   添加客户结果: {'成功' if result else '失败'}")
        
        # 2. 查询所有客户
        print("2. 测试查询所有客户...")
        customers = bank.customer_service.get_customer_info()
        print(f"   客户总数: {len(customers) if customers else 0}")
        
        # 3. 搜索客户
        print("3. 测试搜索客户...")
        search_result = bank.customer_service.search_customers("测试")
        print(f"   搜索结果数量: {len(search_result) if search_result else 0}")
        
        # 4. 更新客户信息
        if customers:
            customer_id = customers[-1]['customerID']  # 使用最后一个客户
            print("4. 测试更新客户信息...")
            result = bank.customer_service.update_customer(customer_id, telephone="13900000002")
            print(f"   更新客户结果: {'成功' if result else '失败'}")
        
        return True
    except Exception as e:
        print(f"客户服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_deposit_service(bank):
    """测试存款类型服务功能"""
    print("\n" + "="*50)
    print("测试存款类型服务功能")
    print("="*50)
    
    try:
        # 1. 添加存款类型
        print("1. 测试添加存款类型...")
        result = bank.deposit_service.add_deposit_type("测试存款", "测试存款类型描述", "1年")
        print(f"   添加存款类型结果: {'成功' if result else '失败'}")
        
        # 2. 查询所有存款类型
        print("2. 测试查询所有存款类型...")
        deposits = bank.deposit_service.get_deposit_types()
        print(f"   存款类型总数: {len(deposits) if deposits else 0}")
        
        return True
    except Exception as e:
        print(f"存款类型服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_card_service(bank):
    """测试银行卡服务功能"""
    print("\n" + "="*50)
    print("测试银行卡服务功能")
    print("="*50)
    
    try:
        # 获取客户和存款类型
        customers = bank.customer_service.get_customer_info()
        deposits = bank.deposit_service.get_deposit_types()
        
        if not customers or not deposits:
            print("   需要先有客户和存款类型数据")
            return False
        
        customer_id = customers[0]['customerID']
        saving_id = deposits[0]['savingID']
        
        # 1. 添加银行卡
        print("1. 测试添加银行卡...")
        test_card_id = "9999888877776666"
        result = bank.card_service.add_card(test_card_id, saving_id, 100.0, 100.0, customer_id)
        print(f"   添加银行卡结果: {'成功' if result else '失败'}")
        
        # 2. 查询银行卡
        print("2. 测试查询银行卡...")
        cards = bank.card_service.get_card_info()
        print(f"   银行卡总数: {len(cards) if cards else 0}")
        
        # 3. 存款操作
        print("3. 测试存款操作...")
        result = bank.card_service.deposit(test_card_id, 50.0)
        print(f"   存款结果: {'成功' if result else '失败'}")
        
        # 4. 查询余额
        print("4. 测试查询余额...")
        balance = bank.card_service.check_balance(test_card_id)
        print(f"   当前余额: {balance}")
        
        # 5. 取款操作
        print("5. 测试取款操作...")
        result = bank.card_service.withdraw(test_card_id, 30.0)
        print(f"   取款结果: {'成功' if result else '失败'}")
        
        # 6. 再次查询余额
        balance = bank.card_service.check_balance(test_card_id)
        print(f"   取款后余额: {balance}")
        
        return True
    except Exception as e:
        print(f"银行卡服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_transaction_service(bank):
    """测试交易服务功能"""
    print("\n" + "="*50)
    print("测试交易服务功能")
    print("="*50)
    
    try:
        # 1. 查询所有交易记录
        print("1. 测试查询所有交易记录...")
        transactions = bank.transaction_service.get_transactions()
        print(f"   交易记录总数: {len(transactions) if transactions else 0}")
        
        # 2. 按卡号查询交易记录
        if transactions:
            card_id = transactions[0]['cardID']
            print("2. 测试按卡号查询交易记录...")
            card_transactions = bank.transaction_service.get_transactions(card_id=card_id)
            print(f"   该卡交易记录数: {len(card_transactions) if card_transactions else 0}")
        
        # 3. 按日期范围查询
        print("3. 测试按日期范围查询...")
        today = datetime.now().strftime("%Y-%m-%d")
        date_transactions = bank.transaction_service.get_transactions(
            start_date=today, end_date=today)
        print(f"   今日交易记录数: {len(date_transactions) if date_transactions else 0}")
        
        return True
    except Exception as e:
        print(f"交易服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_report_service(bank):
    """测试报表服务功能"""
    print("\n" + "="*50)
    print("测试报表服务功能")
    print("="*50)
    
    try:
        # 1. 生成交易明细报表
        print("1. 测试生成交易明细报表...")
        today = datetime.now().strftime("%Y-%m-%d")
        result = bank.report_service.generate_report("交易明细", today, today)
        print(f"   生成交易明细报表结果: {'成功' if result else '失败'}")
        
        # 2. 获取账户统计
        print("2. 测试获取账户统计...")
        stats = bank.report_service.get_account_statistics()
        print(f"   账户统计记录数: {len(stats) if stats else 0}")
        
        return True
    except Exception as e:
        print(f"报表服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_transfer_function(bank):
    """测试转账功能"""
    print("\n" + "="*50)
    print("测试转账功能")
    print("="*50)
    
    try:
        # 获取两张银行卡进行转账测试
        cards = bank.card_service.get_card_info()
        if len(cards) < 2:
            print("   需要至少两张银行卡进行转账测试")
            return False
        
        from_card = cards[0]['cardID']
        to_card = cards[1]['cardID']
        
        # 查询转账前余额
        from_balance_before = bank.card_service.check_balance(from_card)
        to_balance_before = bank.card_service.check_balance(to_card)
        print(f"   转账前 - 转出卡余额: {from_balance_before}, 转入卡余额: {to_balance_before}")
        
        # 执行转账
        print("1. 测试转账功能...")
        result = bank.card_service.transfer(from_card, to_card, 10.0, "测试转账")
        print(f"   转账结果: {'成功' if result else '失败'}")
        
        # 查询转账后余额
        from_balance_after = bank.card_service.check_balance(from_card)
        to_balance_after = bank.card_service.check_balance(to_card)
        print(f"   转账后 - 转出卡余额: {from_balance_after}, 转入卡余额: {to_balance_after}")
        
        return True
    except Exception as e:
        print(f"转账功能测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("银行管理系统全功能测试")
    print("="*60)
    
    try:
        # 初始化系统
        print("正在初始化银行系统...")
        bank = BankSystem()
        print("银行系统初始化成功")
        
        # 执行各项测试
        test_results = []
        
        test_results.append(("客户服务", test_customer_service(bank)))
        test_results.append(("存款类型服务", test_deposit_service(bank)))
        test_results.append(("银行卡服务", test_card_service(bank)))
        test_results.append(("交易服务", test_transaction_service(bank)))
        test_results.append(("报表服务", test_report_service(bank)))
        test_results.append(("转账功能", test_transfer_function(bank)))
        
        # 输出测试结果汇总
        print("\n" + "="*60)
        print("测试结果汇总")
        print("="*60)
        
        success_count = 0
        for test_name, result in test_results:
            status = "✓ 通过" if result else "✗ 失败"
            print(f"{test_name:<15} {status}")
            if result:
                success_count += 1
        
        print(f"\n总计: {success_count}/{len(test_results)} 项测试通过")
        
        # 关闭系统
        bank.close()
        print("\n测试完成，系统已关闭")
        
    except Exception as e:
        print(f"测试过程中出现严重错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
