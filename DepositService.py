# 存款类型服务类 - 管理银行存款产品类型
from BaseService import BaseService


class DepositService(BaseService):
    def add_deposit_type(self, saving_name, descrip, term=None):
        """
        添加存款类型
        Args:
            saving_name: 存款类型名称
            descrip: 存款类型描述
            term: 存款期限（可选，如1年、2年、3年）
        Returns:
            bool: 添加成功返回True，失败返回False
        """
        if term:
            query = "INSERT INTO deposit (savingName, descrip, term) VALUES (%s, %s, %s)"
            return self.db.execute_query(query, (saving_name, descrip, term), fetch=False)
        else:
            query = "INSERT INTO deposit (savingName, descrip) VALUES (%s, %s)"
            return self.db.execute_query(query, (saving_name, descrip), fetch=False)
    
    def get_deposit_types(self, saving_id=None):
        """
        查询存款类型信息
        Args:
            saving_id: 存款类型ID（可选，不提供则查询所有类型）
        Returns:
            查询结果列表
        """
        if saving_id:
            query = "SELECT * FROM deposit WHERE savingID = %s"
            return self.db.execute_query(query, (saving_id,))
        else:
            query = "SELECT * FROM deposit ORDER BY savingID"
            return self.db.execute_query(query)
    
    def update_deposit_type(self, saving_id, saving_name=None, descrip=None, term=None):
        """
        修改存款类型信息
        Args:
            saving_id: 存款类型ID
            saving_name: 新存款类型名称（可选）
            descrip: 新描述（可选）
            term: 新期限（可选）
        Returns:
            bool: 修改成功返回True，失败返回False
        """
        updates = []
        params = []
        
        # 构建动态更新语句
        if saving_name:
            updates.append("savingName = %s")
            params.append(saving_name)
        if descrip:
            updates.append("descrip = %s")
            params.append(descrip)
        if term is not None:  # 允许设置为NULL
            updates.append("term = %s")
            params.append(term)
        
        if not updates:
            print("没有提供要更新的信息")
            return False
        
        params.append(saving_id)
        query = f"UPDATE deposit SET {', '.join(updates)} WHERE savingID = %s"
        return self.db.execute_query(query, params, fetch=False)
    
    def delete_deposit_type(self, saving_id):
        """
        删除存款类型
        Args:
            saving_id: 存款类型ID
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        # 检查是否有银行卡使用此存款类型
        check_query = "SELECT COUNT(*) as count FROM cardInfo WHERE savingID = %s"
        result = self.db.execute_query(check_query, (saving_id,))
        
        if result and result[0]['count'] > 0:
            print(f"无法删除：仍有 {result[0]['count']} 张银行卡使用此存款类型")
            return False
        
        query = "DELETE FROM deposit WHERE savingID = %s"
        return self.db.execute_query(query, (saving_id,), fetch=False)
    
    def get_deposit_statistics(self):
        """
        获取存款类型统计信息
        Returns:
            统计结果列表
        """
        query = """
            SELECT 
                d.savingID,
                d.savingName,
                d.descrip,
                d.term,
                COUNT(c.cardID) as cardCount,
                COALESCE(SUM(c.balance), 0) as totalBalance
            FROM deposit d
            LEFT JOIN cardInfo c ON d.savingID = c.savingID
            GROUP BY d.savingID, d.savingName, d.descrip, d.term
            ORDER BY d.savingID
        """
        return self.db.execute_query(query)
