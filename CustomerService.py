# 客户服务类 - 处理客户信息的增删改查操作
from BaseService import BaseService


class CustomerService(BaseService):
    def add_customer(self, name, pid, telephone, address=None):
        """
        添加新客户
        Args:
            name: 客户姓名
            pid: 身份证号
            telephone: 电话号码
            address: 地址（可选）
        Returns:
            bool: 添加成功返回True，失败返回False
        """
        # 输入数据验证
        if not name or not pid or not telephone:
            print("姓名、身份证号和电话不能为空")
            return False
        
        if len(pid) != 18:
            print("身份证号必须为18位")
            return False
            
        # 插入客户信息到数据库
        query = "INSERT INTO userInfo (customerName, PID, telephone, address) VALUES (%s, %s, %s, %s)"
        return self.db.execute_query(query, (name, pid, telephone, address), fetch=False)
    
    def get_customer_info(self, customer_id=None):
        """
        查询客户信息
        Args:
            customer_id: 客户ID（可选，不提供则查询所有客户）
        Returns:
            查询结果列表
        """
        if customer_id:
            query = "SELECT * FROM userInfo WHERE customerID = %s"
            return self.db.execute_query(query, (customer_id,))
        else:
            query = "SELECT * FROM userInfo"
            return self.db.execute_query(query)
    
    def update_customer(self, customer_id, name=None, telephone=None, address=None):
        """
        修改客户信息
        Args:
            customer_id: 客户ID
            name: 新姓名（可选）
            telephone: 新电话（可选）
            address: 新地址（可选）
        Returns:
            bool: 修改成功返回True，失败返回False
        """
        updates = []
        params = []
        
        # 构建动态更新语句
        if name:
            updates.append("customerName = %s")
            params.append(name)
        if telephone:
            updates.append("telephone = %s")
            params.append(telephone)
        if address:
            updates.append("address = %s")
            params.append(address)
        
        if not updates:
            print("没有提供要更新的信息")
            return False
        
        params.append(customer_id)
        query = f"UPDATE userInfo SET {', '.join(updates)} WHERE customerID = %s"
        return self.db.execute_query(query, params, fetch=False)
    
    def delete_customer(self, customer_id):
        """
        删除客户信息
        Args:
            customer_id: 客户ID
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        query = "DELETE FROM userInfo WHERE customerID = %s"
        return self.db.execute_query(query, (customer_id,), fetch=False)
    
    def search_customers(self, keyword):
        """
        模糊搜索客户信息
        Args:
            keyword: 搜索关键词
        Returns:
            匹配的客户信息列表
        """
        query = """
            SELECT * FROM userInfo 
            WHERE customerName LIKE %s OR telephone LIKE %s OR PID LIKE %s
        """
        search_term = f"%{keyword}%"
        return self.db.execute_query(query, (search_term, search_term, search_term))
