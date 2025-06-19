# 数据库连接类 - 负责管理MySQL数据库连接
import mysql.connector
from mysql.connector import Error


class DatabaseConnector:
    def __init__(self, host='localhost', user='root', password='QAZwsx0823', database='银行'):
        """
        初始化数据库连接参数
        Args:
            host: 数据库主机地址
            user: 数据库用户名
            password: 数据库密码
            database: 数据库名称
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None  # 数据库连接对象
        self.cursor = None      # 数据库游标对象，用于执行SQL语句

    def connect(self):
        """
        连接到MySQL数据库
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                # 使用字典游标，返回结果为字典格式，便于处理
                self.cursor = self.connection.cursor(dictionary=True)
                print("成功连接到MySQL数据库")
                self._create_tables_if_not_exist()  # 自动创建表
                return True
        except Error as e:
            print(f"连接数据库时出错: {e}")
            return False

    def _create_tables_if_not_exist(self):
        """创建表和初始数据（如果不存在）"""
        try:
            # 创建用户信息表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS userInfo (
                  customerID INT PRIMARY KEY AUTO_INCREMENT,
                  customerName VARCHAR(50) NOT NULL,
                  PID CHAR(18) NOT NULL UNIQUE,
                  telephone CHAR(11) NOT NULL,
                  address VARCHAR(50)
                )
            """)

            # 创建存款类型表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS deposit (
                  savingID INT PRIMARY KEY AUTO_INCREMENT,
                  savingName VARCHAR(20) NOT NULL,
                  descrip TEXT NOT NULL,
                  term ENUM('1年', '2年', '3年') NULL
                )
            """)

            # 创建银行卡表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cardInfo (
                  cardID CHAR(16) PRIMARY KEY,
                  curID VARCHAR(10) DEFAULT 'RMB',
                  savingID INT NOT NULL,
                  openDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  openMoney NUMERIC(18,2) NOT NULL,
                  balance NUMERIC(18,2) NOT NULL,
                  pass CHAR(6) DEFAULT '888888',
                  IsReportLoss VARCHAR(3) DEFAULT '否',
                  customerID INT NOT NULL,
                  FOREIGN KEY (customerID) REFERENCES userInfo(customerID) ON UPDATE CASCADE
                )
            """)

            # 创建交易信息表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tradeInfo (
                  tradeID INT AUTO_INCREMENT PRIMARY KEY,
                  cardID CHAR(16) NOT NULL,
                  tradeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  tradeMoney NUMERIC(18,2) NOT NULL CHECK (tradeMoney > 0),
                  tradeType ENUM('存入', '支取') NOT NULL,
                  remark TEXT,
                  FOREIGN KEY (cardID) REFERENCES cardInfo(cardID)
                )
            """)

            # 创建报表表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Report (
                  ReportID INT AUTO_INCREMENT PRIMARY KEY,
                  ReportType ENUM('交易明细', '月度汇总', '年度汇总', '账户统计') NOT NULL,
                  StartDate DATE NOT NULL,
                  EndDate DATE NOT NULL,
                  GeneratedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  CardID CHAR(16),
                  CustomerID INT,
                  TotalDeposit DECIMAL(18,2) DEFAULT 0,
                  TotalWithdrawal DECIMAL(18,2) DEFAULT 0,
                  TransactionCount INT DEFAULT 0,
                  ExportFormat ENUM('CSV', 'PDF', 'Excel') DEFAULT 'CSV',
                  FOREIGN KEY (CardID) REFERENCES cardInfo(cardID) ON DELETE SET NULL,
                  FOREIGN KEY (CustomerID) REFERENCES userInfo(customerID) ON DELETE SET NULL
                )
            """)

            self.connection.commit()
            self._insert_initial_data()  # 插入初始数据
            print("数据库表创建完成")

        except Error as e:
            print(f"创建表时出错: {e}")

    def _insert_initial_data(self):
        """插入初始测试数据"""
        try:
            # 检查是否已有数据
            self.cursor.execute("SELECT COUNT(*) as count FROM userInfo")
            if self.cursor.fetchone()['count'] > 0:
                return  # 已有数据，不重复插入

            # 插入存款类型
            deposit_data = [
                ('活期', '按存款日结算利息', None),
                ('整存整取', '存款期是1年', '1年'),
                ('整存整取', '存款期是2年', '2年'),
                ('整存整取', '存款期是3年', '3年'),
                ('定活两便', '事先不约定存期', None),
                ('零存整取', '存款期是1年', '1年'),
                ('零存整取', '存款期是2年', '2年'),
                ('零存整取', '存款期是3年', '3年')
            ]

            for name, desc, term in deposit_data:
                if term:
                    self.cursor.execute("INSERT INTO deposit (savingName, descrip, term) VALUES (%s, %s, %s)", (name, desc, term))
                else:
                    self.cursor.execute("INSERT INTO deposit (savingName, descrip) VALUES (%s, %s)", (name, desc))

            # 插入测试客户
            customers = [
                ('John', '110000000000000001', '13900000001', '江苏省南京市'),
                ('Jane', '110000000000000002', '13900000002', None),
                ('Michael', '110000000000000003', '13900000003', None),
                ('Emily', '110000000000000004', '13900000004', None),
                ('David', '110000000000000005', '13900000005', None)
            ]

            for name, pid, phone, addr in customers:
                self.cursor.execute("INSERT INTO userInfo (customerName, PID, telephone, address) VALUES (%s, %s, %s, %s)", (name, pid, phone, addr))

            # 插入测试银行卡
            cards = [
                ('1010357600000001', 'RMB', 1, 1000.00, 1000.00, '888888', '否', 1),
                ('1010357600000002', 'RMB', 2, 1.00, 1.00, '888888', '否', 2),
                ('1010357600000003', 'RMB', 2, 1.00, 1.00, '888888', '否', 3),
                ('1010357600000004', 'RMB', 2, 1.00, 1.00, '888888', '否', 4),
                ('1010357600000005', 'RMB', 3, 500.00, 500.00, '888888', '否', 5)
            ]

            for card_data in cards:
                self.cursor.execute("INSERT INTO cardInfo (cardID, curID, savingID, openMoney, balance, pass, IsReportLoss, customerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", card_data)

            self.connection.commit()
            print("初始测试数据插入完成")

        except Error as e:
            print(f"插入初始数据时出错: {e}")

    def close(self):
        """
        关闭数据库连接和游标
        """
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("数据库连接已关闭")

    def execute_query(self, query, params=None, fetch=True):
        """
        执行SQL查询语句
        Args:
            query: SQL查询语句
            params: 查询参数（防止SQL注入）
            fetch: 是否需要获取查询结果
        Returns:
            查询结果或执行状态
        """
        try:
            # 确保数据库连接有效
            if not self.connection or not self.connection.is_connected():
                self.connect()

            # 执行SQL语句
            self.cursor.execute(query, params or ())

            # 如果是SELECT查询且需要获取结果
            if fetch and query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()

            # 提交事务（对于INSERT、UPDATE、DELETE操作）
            self.connection.commit()
            return True

        except Error as e:
            print(f"执行查询时出错: {e}")
            print(f"出错查询: {query}")
            print(f"参数: {params}")
            # 回滚事务
            if self.connection:
                self.connection.rollback()
            return False
