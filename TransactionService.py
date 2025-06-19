# 交易服务类 - 处理交易记录的查询和管理
from BaseService import BaseService
from datetime import datetime


class TransactionService(BaseService):
    def get_transactions(self, card_id=None, start_date=None, end_date=None):
        """
        查询交易记录
        Args:
            card_id: 银行卡号（可选）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
        Returns:
            交易记录列表
        """
        query = """
            SELECT t.*, c.customerID, u.customerName 
            FROM tradeInfo t
            JOIN cardInfo c ON t.cardID = c.cardID
            JOIN userInfo u ON c.customerID = u.customerID
        """
        conditions = []
        params = []
        
        # 构建动态查询条件
        if card_id:
            conditions.append("t.cardID = %s")
            params.append(card_id)
        if start_date:
            conditions.append("DATE(t.tradeDate) >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("DATE(t.tradeDate) <= %s")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY t.tradeDate DESC"
        return self.db.execute_query(query, params)
    
    def delete_transaction(self, transaction_id):
        """
        删除交易记录
        Args:
            transaction_id: 交易ID
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        query = "DELETE FROM tradeInfo WHERE tradeID = %s"
        return self.db.execute_query(query, (transaction_id,), fetch=False)
    
    def get_monthly_summary(self, start_date, end_date, customer_id=None):
        """
        获取月度汇总数据
        Args:
            start_date: 统计开始日期
            end_date: 统计结束日期
            customer_id: 客户ID（可选）
        Returns:
            月度汇总数据列表
        """
        query = """SELECT 
                     c.cardID, 
                     u.customerName,
                     SUM(CASE WHEN t.tradeType = '存入' THEN t.tradeMoney ELSE 0 END) AS totalDeposit,
                     SUM(CASE WHEN t.tradeType = '支取' THEN t.tradeMoney ELSE 0 END) AS totalWithdrawal,
                     COUNT(t.tradeID) AS transactionCount,
                     c.balance AS currentBalance
                   FROM tradeInfo t
                   JOIN cardInfo c ON t.cardID = c.cardID
                   JOIN userInfo u ON c.customerID = u.customerID
                   WHERE DATE(t.tradeDate) BETWEEN %s AND %s"""
        
        params = [start_date, end_date]
        
        if customer_id:
            query += " AND c.customerID = %s"
            params.append(customer_id)
        
        query += " GROUP BY c.cardID, u.customerName, c.balance ORDER BY u.customerName"
        return self.db.execute_query(query, params)
    
    def get_yearly_summary(self, year, customer_id=None):
        """
        获取年度汇总数据
        Args:
            year: 统计年份
            customer_id: 客户ID（可选）
        Returns:
            年度汇总数据列表
        """
        query = """SELECT 
                     YEAR(t.tradeDate) AS year,
                     MONTH(t.tradeDate) AS month,
                     u.customerName,
                     c.cardID,
                     SUM(CASE WHEN t.tradeType = '存入' THEN t.tradeMoney ELSE 0 END) AS totalDeposit,
                     SUM(CASE WHEN t.tradeType = '支取' THEN t.tradeMoney ELSE 0 END) AS totalWithdrawal,
                     COUNT(t.tradeID) AS transactionCount
                   FROM tradeInfo t
                   JOIN cardInfo c ON t.cardID = c.cardID
                   JOIN userInfo u ON c.customerID = u.customerID
                   WHERE YEAR(t.tradeDate) = %s"""
        
        params = [year]
        
        if customer_id:
            query += " AND c.customerID = %s"
            params.append(customer_id)
        
        query += " GROUP BY YEAR(t.tradeDate), MONTH(t.tradeDate), u.customerName, c.cardID"
        query += " ORDER BY year, month, u.customerName"
        return self.db.execute_query(query, params)
    
    def get_transfer_records(self, card_id=None, start_date=None, end_date=None):
        """
        获取转账记录
        Args:
            card_id: 银行卡号（可选）
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
        Returns:
            转账记录列表
        """
        query = """
            SELECT 
                tf.*,
                u1.customerName as fromCustomerName,
                u2.customerName as toCustomerName
            FROM transferInfo tf
            JOIN cardInfo c1 ON tf.fromCardID = c1.cardID
            JOIN cardInfo c2 ON tf.toCardID = c2.cardID
            JOIN userInfo u1 ON c1.customerID = u1.customerID
            JOIN userInfo u2 ON c2.customerID = u2.customerID
        """
        conditions = []
        params = []
        
        if card_id:
            conditions.append("(tf.fromCardID = %s OR tf.toCardID = %s)")
            params.extend([card_id, card_id])
        if start_date:
            conditions.append("DATE(tf.transferDate) >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("DATE(tf.transferDate) <= %s")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY tf.transferDate DESC"
        return self.db.execute_query(query, params)
