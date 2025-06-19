# 数据库初始化类 - 创建视图、触发器和存储过程
from mysql.connector import Error


class DatabaseInitializer:
    def __init__(self, db_connector):
        """
        初始化数据库初始化器
        Args:
            db_connector: 数据库连接器实例
        """
        self.db = db_connector
    
    def create_transfer_table(self):
        """
        创建转账记录表（如果不存在）
        """
        try:
            query = """
                CREATE TABLE IF NOT EXISTS transferInfo (
                  transferID INT AUTO_INCREMENT PRIMARY KEY,
                  fromCardID CHAR(16) NOT NULL,
                  toCardID CHAR(16) NOT NULL,
                  transferAmount NUMERIC(18,2) NOT NULL CHECK (transferAmount > 0),
                  transferDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  remark TEXT,
                  FOREIGN KEY (fromCardID) REFERENCES cardInfo(cardID),
                  FOREIGN KEY (toCardID) REFERENCES cardInfo(cardID)
                )
            """
            self.db.execute_query(query, fetch=False)
            print("转账记录表 transferInfo 创建成功")
        except Error as e:
            print(f"创建转账记录表时出错: {e}")
    
    def create_views(self):
        """
        创建视图以增强查询友好性
        """
        views = {
            'customer_card_view': """
                CREATE OR REPLACE VIEW customer_card_view AS
                SELECT 
                    u.customerID, u.customerName, u.PID, u.telephone, u.address,
                    c.cardID, c.curID, c.balance, c.openDate, c.IsReportLoss,
                    d.savingName, d.descrip AS depositDescription, d.term
                FROM userInfo u
                JOIN cardInfo c ON u.customerID = c.customerID
                JOIN deposit d ON c.savingID = d.savingID
            """,
            'transaction_detail_view': """
                CREATE OR REPLACE VIEW transaction_detail_view AS
                SELECT 
                    t.tradeID, t.cardID, t.tradeDate, t.tradeMoney, t.tradeType, t.remark,
                    c.customerID, u.customerName, c.balance AS currentBalance
                FROM tradeInfo t
                JOIN cardInfo c ON t.cardID = c.cardID
                JOIN userInfo u ON c.customerID = u.customerID
            """,
            'account_summary_view': """
                CREATE OR REPLACE VIEW account_summary_view AS
                SELECT 
                    u.customerID, u.customerName, u.telephone,
                    COUNT(DISTINCT c.cardID) AS cardCount,
                    COALESCE(SUM(c.balance), 0) AS totalBalance,
                    MAX(c.openDate) AS latestOpenDate,
                    COUNT(t.tradeID) AS transactionCount
                FROM userInfo u
                LEFT JOIN cardInfo c ON u.customerID = c.customerID
                LEFT JOIN tradeInfo t ON c.cardID = t.cardID
                GROUP BY u.customerID, u.customerName, u.telephone
            """
        }
        
        for name, sql in views.items():
            try:
                self.db.execute_query(sql, fetch=False)
                print(f"视图 {name} 创建成功")
            except Error as e:
                print(f"创建视图 {name} 时出错: {e}")
    
    def setup_triggers(self):
        """
        设置触发器和存储过程
        """
        # 检查并创建余额变更触发器
        self._create_balance_trigger()
        
        # 检查并创建转账存储过程
        self._create_transfer_procedure()
    
    def _create_balance_trigger(self):
        """
        创建余额变更触发器
        """
        try:
            # 先检查触发器是否存在
            check_query = """
                SELECT TRIGGER_NAME 
                FROM INFORMATION_SCHEMA.TRIGGERS 
                WHERE TRIGGER_SCHEMA = DATABASE() AND TRIGGER_NAME = 'after_card_balance_update'
            """
            result = self.db.execute_query(check_query)
            
            if not result:
                # 创建触发器
                trigger_sql = """
                    CREATE TRIGGER after_card_balance_update
                    AFTER UPDATE ON cardInfo
                    FOR EACH ROW
                    BEGIN
                      DECLARE operation_type ENUM('存入', '支取');
                      DECLARE amount_diff NUMERIC(18,2);
                      
                      -- 计算余额变化量
                      SET amount_diff = NEW.balance - OLD.balance;
                      
                      -- 确定操作类型
                      IF amount_diff > 0 THEN
                        SET operation_type = '存入';
                      ELSEIF amount_diff < 0 THEN
                        SET operation_type = '支取';
                        SET amount_diff = ABS(amount_diff);
                      END IF;
                      
                      -- 如果有余额变化，记录交易
                      IF amount_diff <> 0 THEN
                        INSERT INTO tradeInfo (cardID, tradeMoney, tradeType, remark)
                        VALUES (NEW.cardID, amount_diff, operation_type, 
                                CONCAT('系统自动记录 - 余额变更: ', OLD.balance, ' → ', NEW.balance));
                      END IF;
                    END
                """
                self.db.execute_query(trigger_sql, fetch=False)
                print("触发器 after_card_balance_update 创建成功")
            else:
                print("触发器 after_card_balance_update 已存在")
                
        except Error as e:
            print(f"创建余额变更触发器时出错: {e}")
    
    def _create_transfer_procedure(self):
        """
        创建转账存储过程
        """
        try:
            # 先检查存储过程是否存在
            check_query = """
                SELECT ROUTINE_NAME 
                FROM INFORMATION_SCHEMA.ROUTINES 
                WHERE ROUTINE_SCHEMA = DATABASE() AND ROUTINE_NAME = 'process_transfer'
            """
            result = self.db.execute_query(check_query)
            
            if not result:
                # 创建存储过程
                procedure_sql = """
                    CREATE PROCEDURE process_transfer(
                      IN p_fromCard CHAR(16),
                      IN p_toCard CHAR(16),
                      IN p_amount NUMERIC(18,2),
                      IN p_remark TEXT
                    )
                    BEGIN
                      DECLARE EXIT HANDLER FOR SQLEXCEPTION
                      BEGIN
                        ROLLBACK;
                        RESIGNAL;
                      END;
                      
                      START TRANSACTION;
                      
                      -- 验证转出卡余额是否充足
                      IF (SELECT balance FROM cardInfo WHERE cardID = p_fromCard) < p_amount THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = '转出卡余额不足';
                      END IF;
                      
                      -- 更新转出卡余额
                      UPDATE cardInfo 
                      SET balance = balance - p_amount 
                      WHERE cardID = p_fromCard;
                      
                      -- 更新转入卡余额
                      UPDATE cardInfo 
                      SET balance = balance + p_amount 
                      WHERE cardID = p_toCard;
                      
                      -- 记录转账信息
                      INSERT INTO transferInfo (fromCardID, toCardID, transferAmount, remark)
                      VALUES (p_fromCard, p_toCard, p_amount, p_remark);
                      
                      -- 记录转出交易
                      INSERT INTO tradeInfo (cardID, tradeMoney, tradeType, remark)
                      VALUES (p_fromCard, p_amount, '支取', 
                              CONCAT('转账至卡号: ', p_toCard, ' - ', IFNULL(p_remark, '')));
                      
                      -- 记录转入交易
                      INSERT INTO tradeInfo (cardID, tradeMoney, tradeType, remark)
                      VALUES (p_toCard, p_amount, '存入', 
                              CONCAT('来自卡号: ', p_fromCard, ' - ', IFNULL(p_remark, '')));
                      
                      COMMIT;
                    END
                """
                self.db.execute_query(procedure_sql, fetch=False)
                print("存储过程 process_transfer 创建成功")
            else:
                print("存储过程 process_transfer 已存在")
                
        except Error as e:
            print(f"创建转账存储过程时出错: {e}")
    
    def initialize_all(self):
        """
        初始化所有数据库对象
        """
        print("开始初始化数据库...")
        self.create_transfer_table()
        self.create_views()
        self.setup_triggers()
        print("数据库初始化完成")
