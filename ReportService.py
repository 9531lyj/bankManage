# 报表服务类 - 生成各种统计报表
from BaseService import BaseService
from datetime import datetime


class ReportService(BaseService):
    def __init__(self, db_connector, transaction_service):
        """
        初始化报表服务
        Args:
            db_connector: 数据库连接器
            transaction_service: 交易服务实例
        """
        super().__init__(db_connector)
        self.transaction_service = transaction_service
    
    def generate_report(self, report_type, start_date, end_date, card_id=None, customer_id=None, export_format='CSV'):
        """
        生成报表
        Args:
            report_type: 报表类型（交易明细、月度汇总、年度汇总、账户统计）
            start_date: 开始日期
            end_date: 结束日期
            card_id: 银行卡号（可选）
            customer_id: 客户ID（可选）
            export_format: 导出格式（默认CSV）
        Returns:
            bool: 生成成功返回True，失败返回False
        """
        try:
            # 首先插入报表记录到Report表
            query = """INSERT INTO Report 
                       (ReportType, StartDate, EndDate, CardID, CustomerID, ExportFormat) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            self.db.execute_query(query, (report_type, start_date, end_date, card_id, customer_id, export_format), fetch=False)
            
            # 根据报表类型获取数据
            data = None
            filename = None
            
            if report_type == '交易明细':
                data = self.transaction_service.get_transactions(card_id, start_date, end_date)
                filename = f"transaction_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                
            elif report_type == '月度汇总':
                data = self.transaction_service.get_monthly_summary(start_date, end_date, customer_id)
                filename = f"monthly_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                
            elif report_type == '年度汇总':
                # 从日期中提取年份
                year = start_date.year if hasattr(start_date, 'year') else int(str(start_date)[:4])
                data = self.transaction_service.get_yearly_summary(year, customer_id)
                filename = f"yearly_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                
            elif report_type == '账户统计':
                data = self.get_account_statistics(customer_id)
                filename = f"account_statistics_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                
            else:
                print("无效的报表类型")
                return False
            
            # 导出数据
            if data:
                success = self.export_to_csv(data, filename)
                if success:
                    print(f"报表生成成功：{filename}")
                return success
            else:
                print("没有数据可生成报表")
                return False
                
        except Exception as e:
            print(f"生成报表时出错: {e}")
            return False
    
    def get_account_statistics(self, customer_id=None):
        """
        获取账户统计数据
        Args:
            customer_id: 客户ID（可选）
        Returns:
            账户统计数据列表
        """
        query = """SELECT 
                     u.customerID,
                     u.customerName,
                     u.telephone,
                     COUNT(DISTINCT c.cardID) AS cardCount,
                     COALESCE(SUM(c.balance), 0) AS totalBalance,
                     COUNT(t.tradeID) AS transactionCount,
                     MAX(c.openDate) AS latestOpenDate
                   FROM userInfo u
                   LEFT JOIN cardInfo c ON u.customerID = c.customerID
                   LEFT JOIN tradeInfo t ON c.cardID = t.cardID"""
        
        params = []
        
        if customer_id:
            query += " WHERE u.customerID = %s"
            params.append(customer_id)
        
        query += " GROUP BY u.customerID, u.customerName, u.telephone ORDER BY u.customerID"
        return self.db.execute_query(query, params)
    
    def get_bank_summary(self):
        """
        获取银行整体统计数据
        Returns:
            银行统计数据
        """
        query = """
            SELECT 
                (SELECT COUNT(*) FROM userInfo) AS totalCustomers,
                (SELECT COUNT(*) FROM cardInfo) AS totalCards,
                (SELECT SUM(balance) FROM cardInfo) AS totalBalance,
                (SELECT COUNT(*) FROM tradeInfo) AS totalTransactions,
                (SELECT COUNT(*) FROM transferInfo) AS totalTransfers
        """
        return self.db.execute_query(query)
    
    def get_deposit_type_report(self):
        """
        获取存款类型统计报表
        Returns:
            存款类型统计数据
        """
        query = """
            SELECT 
                d.savingID,
                d.savingName,
                d.descrip,
                d.term,
                COUNT(c.cardID) AS cardCount,
                COALESCE(SUM(c.balance), 0) AS totalBalance,
                COALESCE(AVG(c.balance), 0) AS avgBalance
            FROM deposit d
            LEFT JOIN cardInfo c ON d.savingID = c.savingID
            GROUP BY d.savingID, d.savingName, d.descrip, d.term
            ORDER BY totalBalance DESC
        """
        return self.db.execute_query(query)
