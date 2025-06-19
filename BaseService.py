# 基础服务类 - 提供通用的数据处理和显示功能
import csv
from datetime import datetime
from tabulate import tabulate


class BaseService:
    def __init__(self, db_connector):
        """
        初始化基础服务
        Args:
            db_connector: 数据库连接器实例
        """
        self.db = db_connector
    
    def export_to_csv(self, data, filename):
        """
        将数据导出为CSV文件
        Args:
            data: 要导出的数据列表（字典格式）
            filename: 导出文件名
        Returns:
            bool: 导出成功返回True，失败返回False
        """
        try:
            if not data:
                print("没有数据可导出")
                return False
            
            # 获取数据字段名作为CSV表头
            keys = data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()  # 写入表头
                writer.writerows(data)  # 写入数据行
            print(f"数据已成功导出到 {filename}")
            return True
        except Exception as e:
            print(f"导出数据时出错: {e}")
            return False
    
    def display_table(self, data, title=None):
        """
        以表格形式显示数据
        Args:
            data: 要显示的数据列表
            title: 表格标题（可选）
        """
        if not data:
            print("没有数据显示")
            return
        
        if title:
            print(f"\n=== {title} ===")
        
        # 使用tabulate库美化表格显示
        print(tabulate(data, headers="keys", tablefmt="grid"))
