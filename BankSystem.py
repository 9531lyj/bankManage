# 银行管理系统主类 - 整合所有功能模块
from DatabaseConnector import DatabaseConnector
from CustomerService import CustomerService
from CardService import CardService
from DepositService import DepositService
from TransactionService import TransactionService
from ReportService import ReportService
from DatabaseInitializer import DatabaseInitializer
from datetime import datetime, date


class BankSystem:
    def __init__(self):
        """
        初始化银行系统
        """
        print("正在启动银行管理系统...")
        
        # 初始化数据库连接
        self.db = DatabaseConnector()
        if not self.db.connect():
            raise Exception("无法连接到数据库，请检查数据库配置")
        
        # 初始化所有服务模块
        self.customer_service = CustomerService(self.db)
        self.card_service = CardService(self.db)
        self.deposit_service = DepositService(self.db)
        self.transaction_service = TransactionService(self.db)
        self.report_service = ReportService(self.db, self.transaction_service)
        
        # 初始化数据库视图、触发器和存储过程
        db_initializer = DatabaseInitializer(self.db)
        db_initializer.initialize_all()
        
        print("银行管理系统启动成功！")
    
    def close(self):
        """
        关闭系统，释放资源
        """
        self.db.close()
        print("系统已安全关闭")
    
    def customer_login(self, card_id, password):
        """
        客户登录验证
        Args:
            card_id: 银行卡号
            password: 密码
        Returns:
            登录成功返回卡片信息，失败返回None
        """
        query = "SELECT * FROM cardInfo WHERE cardID = %s AND pass = %s AND IsReportLoss = '否'"
        result = self.db.execute_query(query, (card_id, password))
        return result[0] if result else None
    
    def main_menu(self):
        """
        系统主菜单
        """
        while True:
            print("\n" + "="*50)
            print("           银行管理系统")
            print("="*50)
            print("1. 管理员登录")
            print("2. 客户登录")
            print("0. 退出系统")
            print("="*50)
            
            choice = input("请选择操作 (0-2): ").strip()
            
            if choice == '1':
                self._admin_login()
            elif choice == '2':
                self._customer_login()
            elif choice == '0':
                self.close()
                print("感谢使用银行管理系统，再见！")
                break
            else:
                print("❌ 无效选择，请重新输入")
    
    def _admin_login(self):
        """
        管理员登录处理
        """
        print("\n--- 管理员登录 ---")
        username = input("请输入管理员用户名: ").strip()
        password = input("请输入管理员密码: ").strip()
        
        # 简单的管理员验证（实际项目中应该从数据库验证）
        if username == "admin" and password == "admin123":
            print("✅ 管理员登录成功")
            self.admin_menu()
        else:
            print("❌ 管理员用户名或密码错误")
    
    def _customer_login(self):
        """
        客户登录处理
        """
        print("\n--- 客户登录 ---")
        card_id = input("请输入银行卡号: ").strip()
        password = input("请输入密码: ").strip()
        
        card_info = self.customer_login(card_id, password)
        if card_info:
            if card_info['IsReportLoss'] == '是':
                print("❌ 该银行卡已挂失，无法登录")
            else:
                print("✅ 登录成功")
                self.customer_menu(card_info)
        else:
            print("❌ 银行卡号或密码错误")
    
    def admin_menu(self):
        """
        管理员功能菜单
        """
        while True:
            print("\n" + "="*50)
            print("         管理员功能菜单")
            print("="*50)
            print("1. 客户信息管理")
            print("2. 银行卡管理")
            print("3. 存款业务管理")
            print("4. 交易记录管理")
            print("5. 报表统计")
            print("0. 返回主菜单")
            print("="*50)
            
            choice = input("请选择功能 (0-5): ").strip()
            
            if choice == '1':
                self.customer_management()
            elif choice == '2':
                self.card_management()
            elif choice == '3':
                self.deposit_management()
            elif choice == '4':
                self.transaction_management()
            elif choice == '5':
                self.report_management()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择，请重新输入")
    
    def customer_menu(self, card_info):
        """
        客户功能菜单
        Args:
            card_info: 客户银行卡信息
        """
        while True:
            # 刷新余额信息
            current_balance = self.card_service.check_balance(card_info['cardID'])
            
            print("\n" + "="*50)
            print("         客户服务菜单")
            print("="*50)
            print(f"当前卡号: {card_info['cardID']}")
            print(f"当前余额: ¥{current_balance:.2f}")
            print("="*50)
            print("1. 存款")
            print("2. 取款")
            print("3. 转账")
            print("4. 查询余额")
            print("5. 挂失")
            print("6. 修改密码")
            print("7. 查看交易记录")
            print("0. 退出登录")
            print("="*50)
            
            choice = input("请选择操作 (0-7): ").strip()
            
            if choice == '1':
                self._handle_deposit(card_info['cardID'])
            elif choice == '2':
                self._handle_withdraw(card_info['cardID'])
            elif choice == '3':
                self._handle_transfer(card_info['cardID'])
            elif choice == '4':
                self._handle_balance_inquiry(card_info['cardID'])
            elif choice == '5':
                if self._handle_report_loss(card_info['cardID']):
                    break  # 挂失后退出登录
            elif choice == '6':
                self._handle_password_change(card_info['cardID'])
            elif choice == '7':
                self._handle_transaction_history(card_info['cardID'])
            elif choice == '0':
                print("退出登录成功")
                break
            else:
                print("❌ 无效选择，请重新输入")

    # ==================== 客户操作处理方法 ====================

    def _handle_deposit(self, card_id):
        """处理存款操作"""
        try:
            amount = float(input("请输入存款金额: "))
            if amount <= 0:
                print("❌ 存款金额必须大于0")
                return

            if self.card_service.deposit(card_id, amount):
                print(f"✅ 存款成功，存入金额: ¥{amount:.2f}")
            else:
                print("❌ 存款失败，请重试")
        except ValueError:
            print("❌ 请输入有效的金额")

    def _handle_withdraw(self, card_id):
        """处理取款操作"""
        try:
            amount = float(input("请输入取款金额: "))
            if amount <= 0:
                print("❌ 取款金额必须大于0")
                return

            if self.card_service.withdraw(card_id, amount):
                print(f"✅ 取款成功，取出金额: ¥{amount:.2f}")
            else:
                print("❌ 取款失败，可能是余额不足")
        except ValueError:
            print("❌ 请输入有效的金额")

    def _handle_transfer(self, card_id):
        """处理转账操作"""
        try:
            to_card = input("请输入转入银行卡号: ").strip()
            if not to_card:
                print("❌ 银行卡号不能为空")
                return

            amount = float(input("请输入转账金额: "))
            if amount <= 0:
                print("❌ 转账金额必须大于0")
                return

            remark = input("请输入备注信息(可选): ").strip()

            if self.card_service.transfer(card_id, to_card, amount, remark):
                print(f"✅ 转账成功，转账金额: ¥{amount:.2f}")
            else:
                print("❌ 转账失败，请检查卡号和余额")
        except ValueError:
            print("❌ 请输入有效的金额")

    def _handle_balance_inquiry(self, card_id):
        """处理余额查询"""
        balance = self.card_service.check_balance(card_id)
        if balance is not None:
            print(f"💰 当前余额: ¥{balance:.2f}")
        else:
            print("❌ 查询余额失败")

    def _handle_report_loss(self, card_id):
        """处理挂失操作"""
        confirm = input("确认要挂失此银行卡吗？(y/n): ").strip().lower()
        if confirm == 'y':
            if self.card_service.report_loss(card_id):
                print("✅ 银行卡挂失成功")
                return True
            else:
                print("❌ 挂失失败")
        return False

    def _handle_password_change(self, card_id):
        """处理密码修改"""
        new_password = input("请输入新密码(6位数字): ").strip()
        if self.card_service.change_card_password(card_id, new_password):
            print("✅ 密码修改成功")
        else:
            print("❌ 密码修改失败")

    def _handle_transaction_history(self, card_id):
        """处理交易记录查询"""
        transactions = self.transaction_service.get_transactions(card_id)
        if transactions:
            self.customer_service.display_table(transactions, "交易记录")
        else:
            print("📝 暂无交易记录")

    # ==================== 管理员功能模块 ====================

    def customer_management(self):
        """客户信息管理"""
        while True:
            print("\n--- 客户信息管理 ---")
            print("1. 添加客户")
            print("2. 查询客户")
            print("3. 修改客户信息")
            print("4. 删除客户")
            print("5. 搜索客户")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self._add_customer()
            elif choice == '2':
                self._query_customers()
            elif choice == '3':
                self._update_customer()
            elif choice == '4':
                self._delete_customer()
            elif choice == '5':
                self._search_customers()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")

    def _add_customer(self):
        """添加客户"""
        print("\n--- 添加新客户 ---")
        name = input("客户姓名: ").strip()
        pid = input("身份证号(18位): ").strip()
        telephone = input("电话号码: ").strip()
        address = input("地址(可选): ").strip() or None

        if self.customer_service.add_customer(name, pid, telephone, address):
            print("✅ 客户添加成功")
        else:
            print("❌ 客户添加失败")

    def _query_customers(self):
        """查询客户"""
        customers = self.customer_service.get_customer_info()
        if customers:
            self.customer_service.display_table(customers, "客户信息列表")
        else:
            print("📝 暂无客户信息")

    def _update_customer(self):
        """修改客户信息"""
        try:
            customer_id = int(input("请输入要修改的客户ID: "))
            print("请输入新信息(留空表示不修改):")
            name = input("新姓名: ").strip() or None
            telephone = input("新电话: ").strip() or None
            address = input("新地址: ").strip() or None

            if self.customer_service.update_customer(customer_id, name, telephone, address):
                print("✅ 客户信息修改成功")
            else:
                print("❌ 客户信息修改失败")
        except ValueError:
            print("❌ 请输入有效的客户ID")

    def _delete_customer(self):
        """删除客户"""
        try:
            customer_id = int(input("请输入要删除的客户ID: "))
            confirm = input(f"确认删除客户ID {customer_id} 吗？(y/n): ").strip().lower()
            if confirm == 'y':
                if self.customer_service.delete_customer(customer_id):
                    print("✅ 客户删除成功")
                else:
                    print("❌ 客户删除失败")
        except ValueError:
            print("❌ 请输入有效的客户ID")

    def _search_customers(self):
        """搜索客户"""
        keyword = input("请输入搜索关键词(姓名/电话/身份证): ").strip()
        if keyword:
            results = self.customer_service.search_customers(keyword)
            if results:
                self.customer_service.display_table(results, f"搜索结果 - '{keyword}'")
            else:
                print("📝 未找到匹配的客户")
        else:
            print("❌ 搜索关键词不能为空")

    def card_management(self):
        """银行卡管理"""
        while True:
            print("\n--- 银行卡管理 ---")
            print("1. 添加银行卡")
            print("2. 查询银行卡")
            print("3. 修改银行卡信息")
            print("4. 删除银行卡")
            print("5. 银行卡挂失")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self._add_card()
            elif choice == '2':
                self._query_cards()
            elif choice == '3':
                self._update_card()
            elif choice == '4':
                self._delete_card()
            elif choice == '5':
                self._report_loss_card()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")

    def _add_card(self):
        """添加银行卡"""
        print("\n--- 添加新银行卡 ---")
        try:
            card_id = input("银行卡号(16位): ").strip()
            customer_id = int(input("客户ID: "))
            saving_id = int(input("存款类型ID: "))
            open_money = float(input("开户金额: "))
            balance = float(input("初始余额: "))

            if self.card_service.add_card(card_id, saving_id, open_money, balance, customer_id):
                print("✅ 银行卡添加成功")
            else:
                print("❌ 银行卡添加失败")
        except ValueError:
            print("❌ 请输入有效的数值")

    def _query_cards(self):
        """查询银行卡"""
        cards = self.card_service.get_card_info()
        if cards:
            self.card_service.display_table(cards, "银行卡信息列表")
        else:
            print("📝 暂无银行卡信息")

    def _update_card(self):
        """修改银行卡信息"""
        card_id = input("请输入要修改的银行卡号: ").strip()
        print("请输入新信息(留空表示不修改):")
        try:
            saving_id_input = input("新存款类型ID: ").strip()
            balance_input = input("新余额: ").strip()

            saving_id = int(saving_id_input) if saving_id_input else None
            balance = float(balance_input) if balance_input else None

            if self.card_service.update_card_info(card_id, saving_id, balance):
                print("✅ 银行卡信息修改成功")
            else:
                print("❌ 银行卡信息修改失败")
        except ValueError:
            print("❌ 请输入有效的数值")

    def _delete_card(self):
        """删除银行卡"""
        card_id = input("请输入要删除的银行卡号: ").strip()
        confirm = input(f"确认删除银行卡 {card_id} 吗？(y/n): ").strip().lower()
        if confirm == 'y':
            if self.card_service.delete_card(card_id):
                print("✅ 银行卡删除成功")
            else:
                print("❌ 银行卡删除失败")

    def _report_loss_card(self):
        """银行卡挂失"""
        card_id = input("请输入要挂失的银行卡号: ").strip()
        if self.card_service.report_loss(card_id):
            print("✅ 银行卡挂失成功")
        else:
            print("❌ 银行卡挂失失败")

    def deposit_management(self):
        """存款业务管理"""
        while True:
            print("\n--- 存款业务管理 ---")
            print("1. 添加存款类型")
            print("2. 查询存款类型")
            print("3. 修改存款类型")
            print("4. 删除存款类型")
            print("5. 存款类型统计")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self._add_deposit_type()
            elif choice == '2':
                self._query_deposit_types()
            elif choice == '3':
                self._update_deposit_type()
            elif choice == '4':
                self._delete_deposit_type()
            elif choice == '5':
                self._deposit_statistics()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")

    def _add_deposit_type(self):
        """添加存款类型"""
        print("\n--- 添加存款类型 ---")
        saving_name = input("存款类型名称: ").strip()
        descrip = input("存款类型描述: ").strip()
        term = input("存款期限(1年/2年/3年，可选): ").strip() or None

        if self.deposit_service.add_deposit_type(saving_name, descrip, term):
            print("✅ 存款类型添加成功")
        else:
            print("❌ 存款类型添加失败")

    def _query_deposit_types(self):
        """查询存款类型"""
        deposits = self.deposit_service.get_deposit_types()
        if deposits:
            self.deposit_service.display_table(deposits, "存款类型列表")
        else:
            print("📝 暂无存款类型")

    def _update_deposit_type(self):
        """修改存款类型"""
        try:
            saving_id = int(input("请输入要修改的存款类型ID: "))
            print("请输入新信息(留空表示不修改):")
            saving_name = input("新存款类型名称: ").strip() or None
            descrip = input("新描述: ").strip() or None
            term = input("新期限: ").strip() or None

            if self.deposit_service.update_deposit_type(saving_id, saving_name, descrip, term):
                print("✅ 存款类型修改成功")
            else:
                print("❌ 存款类型修改失败")
        except ValueError:
            print("❌ 请输入有效的存款类型ID")

    def _delete_deposit_type(self):
        """删除存款类型"""
        try:
            saving_id = int(input("请输入要删除的存款类型ID: "))
            confirm = input(f"确认删除存款类型ID {saving_id} 吗？(y/n): ").strip().lower()
            if confirm == 'y':
                if self.deposit_service.delete_deposit_type(saving_id):
                    print("✅ 存款类型删除成功")
                else:
                    print("❌ 存款类型删除失败")
        except ValueError:
            print("❌ 请输入有效的存款类型ID")

    def _deposit_statistics(self):
        """存款类型统计"""
        stats = self.deposit_service.get_deposit_statistics()
        if stats:
            self.deposit_service.display_table(stats, "存款类型统计")
        else:
            print("📝 暂无统计数据")

    def transaction_management(self):
        """交易记录管理"""
        while True:
            print("\n--- 交易记录管理 ---")
            print("1. 查询所有交易记录")
            print("2. 按卡号查询交易")
            print("3. 按日期查询交易")
            print("4. 查询转账记录")
            print("5. 删除交易记录")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self._query_all_transactions()
            elif choice == '2':
                self._query_transactions_by_card()
            elif choice == '3':
                self._query_transactions_by_date()
            elif choice == '4':
                self._query_transfer_records()
            elif choice == '5':
                self._delete_transaction()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")

    def _query_all_transactions(self):
        """查询所有交易记录"""
        transactions = self.transaction_service.get_transactions()
        if transactions:
            self.transaction_service.display_table(transactions, "所有交易记录")
        else:
            print("📝 暂无交易记录")

    def _query_transactions_by_card(self):
        """按卡号查询交易"""
        card_id = input("请输入银行卡号: ").strip()
        transactions = self.transaction_service.get_transactions(card_id)
        if transactions:
            self.transaction_service.display_table(transactions, f"卡号 {card_id} 的交易记录")
        else:
            print("📝 该卡暂无交易记录")

    def _query_transactions_by_date(self):
        """按日期查询交易"""
        start_date = input("请输入开始日期(YYYY-MM-DD): ").strip()
        end_date = input("请输入结束日期(YYYY-MM-DD): ").strip()
        transactions = self.transaction_service.get_transactions(None, start_date, end_date)
        if transactions:
            self.transaction_service.display_table(transactions, f"{start_date} 至 {end_date} 的交易记录")
        else:
            print("📝 该时间段暂无交易记录")

    def _query_transfer_records(self):
        """查询转账记录"""
        transfers = self.transaction_service.get_transfer_records()
        if transfers:
            self.transaction_service.display_table(transfers, "转账记录")
        else:
            print("📝 暂无转账记录")

    def _delete_transaction(self):
        """删除交易记录"""
        try:
            transaction_id = int(input("请输入要删除的交易ID: "))
            confirm = input(f"确认删除交易ID {transaction_id} 吗？(y/n): ").strip().lower()
            if confirm == 'y':
                if self.transaction_service.delete_transaction(transaction_id):
                    print("✅ 交易记录删除成功")
                else:
                    print("❌ 交易记录删除失败")
        except ValueError:
            print("❌ 请输入有效的交易ID")

    def report_management(self):
        """报表统计管理"""
        while True:
            print("\n--- 报表统计管理 ---")
            print("1. 生成交易明细报表")
            print("2. 生成月度汇总报表")
            print("3. 生成年度汇总报表")
            print("4. 生成账户统计报表")
            print("5. 银行整体统计")
            print("6. 存款类型统计报表")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self._generate_transaction_report()
            elif choice == '2':
                self._generate_monthly_report()
            elif choice == '3':
                self._generate_yearly_report()
            elif choice == '4':
                self._generate_account_report()
            elif choice == '5':
                self._show_bank_summary()
            elif choice == '6':
                self._show_deposit_report()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")

    def _generate_transaction_report(self):
        """生成交易明细报表"""
        start_date = input("请输入开始日期(YYYY-MM-DD): ").strip()
        end_date = input("请输入结束日期(YYYY-MM-DD): ").strip()
        card_id = input("请输入银行卡号(可选): ").strip() or None

        if self.report_service.generate_report('交易明细', start_date, end_date, card_id):
            print("✅ 交易明细报表生成成功")
        else:
            print("❌ 报表生成失败")

    def _generate_monthly_report(self):
        """生成月度汇总报表"""
        start_date = input("请输入开始日期(YYYY-MM-DD): ").strip()
        end_date = input("请输入结束日期(YYYY-MM-DD): ").strip()
        customer_id_input = input("请输入客户ID(可选): ").strip()
        customer_id = int(customer_id_input) if customer_id_input else None

        if self.report_service.generate_report('月度汇总', start_date, end_date, None, customer_id):
            print("✅ 月度汇总报表生成成功")
        else:
            print("❌ 报表生成失败")

    def _generate_yearly_report(self):
        """生成年度汇总报表"""
        year = input("请输入年份(YYYY): ").strip()
        customer_id_input = input("请输入客户ID(可选): ").strip()
        customer_id = int(customer_id_input) if customer_id_input else None

        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        if self.report_service.generate_report('年度汇总', start_date, end_date, None, customer_id):
            print("✅ 年度汇总报表生成成功")
        else:
            print("❌ 报表生成失败")

    def _generate_account_report(self):
        """生成账户统计报表"""
        customer_id_input = input("请输入客户ID(可选): ").strip()
        customer_id = int(customer_id_input) if customer_id_input else None

        today = datetime.now().date()
        if self.report_service.generate_report('账户统计', today, today, None, customer_id):
            print("✅ 账户统计报表生成成功")
        else:
            print("❌ 报表生成失败")

    def _show_bank_summary(self):
        """显示银行整体统计"""
        summary = self.report_service.get_bank_summary()
        if summary:
            self.report_service.display_table(summary, "银行整体统计")
        else:
            print("📝 暂无统计数据")

    def _show_deposit_report(self):
        """显示存款类型统计报表"""
        report = self.report_service.get_deposit_type_report()
        if report:
            self.report_service.display_table(report, "存款类型统计报表")
        else:
            print("📝 暂无统计数据")


# ==================== 主程序入口 ====================

if __name__ == "__main__":
    try:
        # 创建并启动银行系统
        bank_system = BankSystem()
        bank_system.main_menu()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        print("请检查数据库连接配置和依赖库安装")
    finally:
        print("感谢使用银行管理系统！")
