# 银行卡服务类 - 处理银行卡相关的所有操作
from BaseService import BaseService


class CardService(BaseService):
    def add_card(self, card_id, saving_id, open_money, balance, customer_id, passcode='888888', currency='RMB'):
        """
        添加新银行卡
        Args:
            card_id: 银行卡号
            saving_id: 存款类型ID
            open_money: 开户金额
            balance: 当前余额
            customer_id: 客户ID
            passcode: 密码（默认888888）
            currency: 货币类型（默认RMB）
        Returns:
            bool: 添加成功返回True，失败返回False
        """
        query = """INSERT INTO cardInfo 
                   (cardID, curID, savingID, openMoney, balance, pass, customerID) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        return self.db.execute_query(query, (card_id, currency, saving_id, open_money, balance, passcode, customer_id), fetch=False)
    
    def get_card_info(self, card_id=None, customer_id=None):
        """
        查询银行卡信息
        Args:
            card_id: 银行卡号（可选）
            customer_id: 客户ID（可选）
        Returns:
            查询结果列表
        """
        if card_id:
            query = "SELECT * FROM cardInfo WHERE cardID = %s"
            return self.db.execute_query(query, (card_id,))
        elif customer_id:
            query = "SELECT * FROM cardInfo WHERE customerID = %s"
            return self.db.execute_query(query, (customer_id,))
        else:
            # 联合查询，显示客户姓名
            query = """SELECT c.*, u.customerName 
                       FROM cardInfo c 
                       JOIN userInfo u ON c.customerID = u.customerID"""
            return self.db.execute_query(query)
    
    def report_loss(self, card_id):
        """
        挂失银行卡
        Args:
            card_id: 银行卡号
        Returns:
            bool: 挂失成功返回True，失败返回False
        """
        query = "UPDATE cardInfo SET IsReportLoss = '是' WHERE cardID = %s"
        return self.db.execute_query(query, (card_id,), fetch=False)
    
    def change_card_password(self, card_id, new_password):
        """
        修改银行卡密码
        Args:
            card_id: 银行卡号
            new_password: 新密码
        Returns:
            bool: 修改成功返回True，失败返回False
        """
        # 密码复杂度检查
        if len(new_password) != 6 or not new_password.isdigit():
            print("密码必须为6位数字")
            return False
            
        query = "UPDATE cardInfo SET pass = %s WHERE cardID = %s"
        return self.db.execute_query(query, (new_password, card_id), fetch=False)
    
    def update_card_info(self, card_id, saving_id=None, balance=None):
        """
        修改银行卡信息
        Args:
            card_id: 银行卡号
            saving_id: 新存款类型ID（可选）
            balance: 新余额（可选）
        Returns:
            bool: 修改成功返回True，失败返回False
        """
        updates = []
        params = []
        
        if saving_id:
            updates.append("savingID = %s")
            params.append(saving_id)
        if balance is not None:
            updates.append("balance = %s")
            params.append(balance)
        
        if not updates:
            print("没有提供要更新的信息")
            return False
        
        params.append(card_id)
        query = f"UPDATE cardInfo SET {', '.join(updates)} WHERE cardID = %s"
        return self.db.execute_query(query, params, fetch=False)
    
    def delete_card(self, card_id):
        """
        删除银行卡
        Args:
            card_id: 银行卡号
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        query = "DELETE FROM cardInfo WHERE cardID = %s"
        return self.db.execute_query(query, (card_id,), fetch=False)
    
    def deposit(self, card_id, amount):
        """
        存款操作（通过触发器自动记录交易）
        Args:
            card_id: 银行卡号
            amount: 存款金额
        Returns:
            bool: 存款成功返回True，失败返回False
        """
        if amount <= 0:
            print("存款金额必须大于0")
            return False
        query = "UPDATE cardInfo SET balance = balance + %s WHERE cardID = %s"
        return self.db.execute_query(query, (amount, card_id), fetch=False)
    
    def withdraw(self, card_id, amount):
        """
        取款操作（通过触发器自动记录交易）
        Args:
            card_id: 银行卡号
            amount: 取款金额
        Returns:
            bool: 取款成功返回True，失败返回False
        """
        if amount <= 0:
            print("取款金额必须大于0")
            return False
        # 检查余额是否充足
        query = "UPDATE cardInfo SET balance = balance - %s WHERE cardID = %s AND balance >= %s"
        result = self.db.execute_query(query, (amount, card_id, amount), fetch=False)
        if not result:
            print("余额不足或卡号不存在")
        return result
    
    def check_balance(self, card_id):
        """
        查询余额
        Args:
            card_id: 银行卡号
        Returns:
            余额金额或None
        """
        query = "SELECT balance FROM cardInfo WHERE cardID = %s"
        result = self.db.execute_query(query, (card_id,))
        return result[0]['balance'] if result else None
    
    def transfer(self, from_card, to_card, amount, remark=None):
        """
        转账操作（调用存储过程）
        Args:
            from_card: 转出卡号
            to_card: 转入卡号
            amount: 转账金额
            remark: 备注信息
        Returns:
            bool: 转账成功返回True，失败返回False
        """
        if amount <= 0:
            print("转账金额必须大于0")
            return False
        query = "CALL process_transfer(%s, %s, %s, %s)"
        return self.db.execute_query(query, (from_card, to_card, amount, remark), fetch=False)
