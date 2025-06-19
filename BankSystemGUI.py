#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行管理系统GUI界面
使用tkinter创建现代化的图形用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkFont
import threading
from datetime import datetime, date
from BankSystem import BankSystem
from DatabaseConnector import DatabaseConnector
from CustomerService import CustomerService
from CardService import CardService
from DepositService import DepositService
from TransactionService import TransactionService
from ReportService import ReportService


class BankSystemGUI:
    def __init__(self):
        """初始化GUI界面"""
        self.root = tk.Tk()
        self.root.title("银行管理系统")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # 设置窗口图标和样式
        self.setup_styles()
        
        # 初始化银行系统
        self.bank_system = None
        self.current_user = None
        self.user_type = None  # 'admin' 或 'customer'
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 显示登录界面
        self.show_login_screen()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置样式
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        style.configure('Success.TLabel', font=('Arial', 10), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Arial', 10), foreground='#e74c3c')

        # 按钮样式
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Arial', 9))

    def center_dialog(self, dialog):
        """居中显示对话框"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
    def clear_frame(self):
        """清空主框架"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def show_login_screen(self):
        """显示登录界面"""
        self.clear_frame()
        
        # 创建登录框架
        login_frame = ttk.Frame(self.main_frame)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 标题
        title_label = ttk.Label(login_frame, text="银行管理系统", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # 登录选项框架
        options_frame = ttk.Frame(login_frame)
        options_frame.pack(pady=10)
        
        # 管理员登录按钮
        admin_btn = ttk.Button(options_frame, text="管理员登录", 
                              command=self.show_admin_login, 
                              style='Primary.TButton', width=15)
        admin_btn.pack(pady=5)
        
        # 客户登录按钮
        customer_btn = ttk.Button(options_frame, text="客户登录", 
                                 command=self.show_customer_login, 
                                 style='Primary.TButton', width=15)
        customer_btn.pack(pady=5)
        
        # 系统信息
        info_label = ttk.Label(login_frame, text="请选择登录方式", style='Info.TLabel')
        info_label.pack(pady=(20, 0))
        
    def show_admin_login(self):
        """显示管理员登录界面"""
        self.clear_frame()
        
        # 创建登录表单
        form_frame = ttk.Frame(self.main_frame)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 标题
        title_label = ttk.Label(form_frame, text="管理员登录", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 用户名输入
        ttk.Label(form_frame, text="用户名:", style='Heading.TLabel').pack(anchor=tk.W)
        self.admin_username = ttk.Entry(form_frame, width=25, font=('Arial', 11))
        self.admin_username.pack(pady=(5, 10))
        self.admin_username.insert(0, "admin")  # 默认值
        
        # 密码输入
        ttk.Label(form_frame, text="密码:", style='Heading.TLabel').pack(anchor=tk.W)
        self.admin_password = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 11))
        self.admin_password.pack(pady=(5, 20))
        self.admin_password.insert(0, "admin123")  # 默认值
        
        # 按钮框架
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack()
        
        # 登录按钮
        login_btn = ttk.Button(btn_frame, text="登录", command=self.admin_login, 
                              style='Primary.TButton', width=10)
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 返回按钮
        back_btn = ttk.Button(btn_frame, text="返回", command=self.show_login_screen, 
                             style='Secondary.TButton', width=10)
        back_btn.pack(side=tk.LEFT)
        
        # 绑定回车键
        self.admin_password.bind('<Return>', lambda e: self.admin_login())
        
    def show_customer_login(self):
        """显示客户登录界面"""
        self.clear_frame()
        
        # 创建登录表单
        form_frame = ttk.Frame(self.main_frame)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 标题
        title_label = ttk.Label(form_frame, text="客户登录", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 卡号输入
        ttk.Label(form_frame, text="银行卡号:", style='Heading.TLabel').pack(anchor=tk.W)
        self.customer_cardid = ttk.Entry(form_frame, width=25, font=('Arial', 11))
        self.customer_cardid.pack(pady=(5, 10))
        self.customer_cardid.insert(0, "1010357600000001")  # 默认测试卡号
        
        # 密码输入
        ttk.Label(form_frame, text="密码:", style='Heading.TLabel').pack(anchor=tk.W)
        self.customer_password = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 11))
        self.customer_password.pack(pady=(5, 20))
        self.customer_password.insert(0, "888888")  # 默认密码
        
        # 按钮框架
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack()
        
        # 登录按钮
        login_btn = ttk.Button(btn_frame, text="登录", command=self.customer_login, 
                              style='Primary.TButton', width=10)
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 返回按钮
        back_btn = ttk.Button(btn_frame, text="返回", command=self.show_login_screen, 
                             style='Secondary.TButton', width=10)
        back_btn.pack(side=tk.LEFT)
        
        # 绑定回车键
        self.customer_password.bind('<Return>', lambda e: self.customer_login())
        
    def admin_login(self):
        """管理员登录验证"""
        username = self.admin_username.get().strip()
        password = self.admin_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
            
        # 简单验证（实际项目中应该从数据库验证）
        if username == "admin" and password == "admin123":
            self.user_type = "admin"
            self.current_user = {"username": username}
            self.initialize_bank_system()
        else:
            messagebox.showerror("登录失败", "用户名或密码错误")
            
    def customer_login(self):
        """客户登录验证"""
        card_id = self.customer_cardid.get().strip()
        password = self.customer_password.get().strip()
        
        if not card_id or not password:
            messagebox.showerror("错误", "请输入卡号和密码")
            return
            
        # 初始化银行系统进行验证
        try:
            if not self.bank_system:
                self.bank_system = BankSystem()
            
            # 验证客户登录
            card_info = self.bank_system.customer_login(card_id, password)
            if card_info:
                if card_info['IsReportLoss'] == '是':
                    messagebox.showerror("登录失败", "该银行卡已挂失，无法登录")
                    return
                    
                self.user_type = "customer"
                self.current_user = card_info
                self.show_customer_main()
            else:
                messagebox.showerror("登录失败", "卡号或密码错误")
                
        except Exception as e:
            messagebox.showerror("系统错误", f"登录时发生错误: {str(e)}")
            
    def initialize_bank_system(self):
        """初始化银行系统并显示主界面"""
        try:
            # 显示加载提示
            loading_label = ttk.Label(self.main_frame, text="正在初始化系统...", style='Info.TLabel')
            loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.root.update()
            
            # 在后台线程中初始化
            def init_system():
                try:
                    self.bank_system = BankSystem()
                    # 初始化完成后切换到主界面
                    self.root.after(0, self.show_admin_main)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("系统错误", f"系统初始化失败: {str(e)}"))
                    self.root.after(0, self.show_login_screen)
            
            thread = threading.Thread(target=init_system)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("系统错误", f"系统初始化失败: {str(e)}")
            self.show_login_screen()

    def show_admin_main(self):
        """显示管理员主界面"""
        self.clear_frame()

        # 创建顶部工具栏
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        # 欢迎信息
        welcome_label = ttk.Label(toolbar, text=f"欢迎，管理员 {self.current_user['username']}",
                                 style='Title.TLabel')
        welcome_label.pack(side=tk.LEFT)

        # 退出按钮
        logout_btn = ttk.Button(toolbar, text="退出登录", command=self.logout,
                               style='Secondary.TButton')
        logout_btn.pack(side=tk.RIGHT)

        # 创建主要内容区域
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧菜单
        menu_frame = ttk.LabelFrame(content_frame, text="功能菜单", padding=10)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 菜单按钮
        menu_buttons = [
            ("客户管理", self.show_customer_management),
            ("银行卡管理", self.show_card_management),
            ("存款类型管理", self.show_deposit_management),
            ("交易记录查询", self.show_transaction_query),
            ("报表生成", self.show_report_management),
            ("系统统计", self.show_system_statistics)
        ]

        for text, command in menu_buttons:
            btn = ttk.Button(menu_frame, text=text, command=command,
                           style='Primary.TButton', width=15)
            btn.pack(pady=5, fill=tk.X)

        # 右侧工作区域
        self.work_frame = ttk.LabelFrame(content_frame, text="工作区域", padding=10)
        self.work_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 显示欢迎信息
        welcome_text = ttk.Label(self.work_frame,
                               text="欢迎使用银行管理系统\n\n请从左侧菜单选择功能",
                               style='Info.TLabel', justify=tk.CENTER)
        welcome_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def show_customer_main(self):
        """显示客户主界面"""
        self.clear_frame()

        # 创建顶部工具栏
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        # 客户信息
        card_info = self.current_user
        welcome_label = ttk.Label(toolbar,
                                 text=f"卡号: {card_info['cardID']} | 余额: ¥{card_info['balance']}",
                                 style='Title.TLabel')
        welcome_label.pack(side=tk.LEFT)

        # 退出按钮
        logout_btn = ttk.Button(toolbar, text="退出登录", command=self.logout,
                               style='Secondary.TButton')
        logout_btn.pack(side=tk.RIGHT)

        # 刷新余额按钮
        refresh_btn = ttk.Button(toolbar, text="刷新余额", command=self.refresh_balance,
                                style='Secondary.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=(0, 10))

        # 创建主要内容区域
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧菜单
        menu_frame = ttk.LabelFrame(content_frame, text="银行业务", padding=10)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 菜单按钮
        menu_buttons = [
            ("存款", self.customer_deposit),
            ("取款", self.customer_withdraw),
            ("转账", self.customer_transfer),
            ("查询余额", self.customer_check_balance),
            ("交易记录", self.customer_transaction_history),
            ("修改密码", self.customer_change_password),
            ("银行卡挂失", self.customer_report_loss)
        ]

        for text, command in menu_buttons:
            btn = ttk.Button(menu_frame, text=text, command=command,
                           style='Primary.TButton', width=12)
            btn.pack(pady=5, fill=tk.X)

        # 右侧工作区域
        self.work_frame = ttk.LabelFrame(content_frame, text="操作区域", padding=10)
        self.work_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 显示账户信息
        self.show_account_info()

    def logout(self):
        """退出登录"""
        if self.bank_system:
            self.bank_system.close()
            self.bank_system = None
        self.current_user = None
        self.user_type = None
        self.show_login_screen()

    def refresh_balance(self):
        """刷新客户余额"""
        try:
            card_id = self.current_user['cardID']
            balance = self.bank_system.card_service.check_balance(card_id)
            if balance is not None:
                self.current_user['balance'] = balance
                self.show_customer_main()  # 重新显示界面以更新余额
            else:
                messagebox.showerror("错误", "无法获取余额信息")
        except Exception as e:
            messagebox.showerror("错误", f"刷新余额失败: {str(e)}")

    def show_account_info(self):
        """显示账户信息"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        info_frame = ttk.Frame(self.work_frame)
        info_frame.pack(fill=tk.BOTH, expand=True)

        # 账户信息标题
        title_label = ttk.Label(info_frame, text="账户信息", style='Heading.TLabel')
        title_label.pack(pady=(0, 20))

        # 账户详情
        card_info = self.current_user
        info_text = f"""
卡号: {card_info['cardID']}
当前余额: ¥{card_info['balance']}
货币类型: {card_info['curID']}
开户日期: {card_info['openDate']}
挂失状态: {card_info['IsReportLoss']}
        """

        info_label = ttk.Label(info_frame, text=info_text.strip(),
                              style='Info.TLabel', justify=tk.LEFT)
        info_label.pack(anchor=tk.W)

    def customer_deposit(self):
        """客户存款操作"""
        amount = simpledialog.askfloat("存款", "请输入存款金额:", minvalue=0.01)
        if amount:
            try:
                if self.bank_system.card_service.deposit(self.current_user['cardID'], amount):
                    messagebox.showinfo("成功", f"存款成功！存入金额: ¥{amount}")
                    self.refresh_balance()
                else:
                    messagebox.showerror("失败", "存款操作失败")
            except Exception as e:
                messagebox.showerror("错误", f"存款失败: {str(e)}")

    def customer_withdraw(self):
        """客户取款操作"""
        amount = simpledialog.askfloat("取款", "请输入取款金额:", minvalue=0.01)
        if amount:
            try:
                if self.bank_system.card_service.withdraw(self.current_user['cardID'], amount):
                    messagebox.showinfo("成功", f"取款成功！取出金额: ¥{amount}")
                    self.refresh_balance()
                else:
                    messagebox.showerror("失败", "取款失败，可能是余额不足")
            except Exception as e:
                messagebox.showerror("错误", f"取款失败: {str(e)}")

    def customer_transfer(self):
        """客户转账操作"""
        # 创建转账对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("转账")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # 居中显示
        self.center_dialog(dialog)

        # 转账表单
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="转账", style='Title.TLabel').pack(pady=(0, 20))

        # 转入卡号
        ttk.Label(form_frame, text="转入卡号:", style='Heading.TLabel').pack(anchor=tk.W)
        to_card_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        to_card_entry.pack(pady=(5, 10), fill=tk.X)

        # 转账金额
        ttk.Label(form_frame, text="转账金额:", style='Heading.TLabel').pack(anchor=tk.W)
        amount_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        amount_entry.pack(pady=(5, 10), fill=tk.X)

        # 备注
        ttk.Label(form_frame, text="备注(可选):", style='Heading.TLabel').pack(anchor=tk.W)
        remark_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        remark_entry.pack(pady=(5, 20), fill=tk.X)

        def do_transfer():
            to_card = to_card_entry.get().strip()
            try:
                amount = float(amount_entry.get().strip())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的金额")
                return

            remark = remark_entry.get().strip()

            if not to_card:
                messagebox.showerror("错误", "请输入转入卡号")
                return

            if amount <= 0:
                messagebox.showerror("错误", "转账金额必须大于0")
                return

            try:
                if self.bank_system.card_service.transfer(self.current_user['cardID'],
                                                        to_card, amount, remark):
                    messagebox.showinfo("成功", f"转账成功！\n转入卡号: {to_card}\n金额: ¥{amount}")
                    dialog.destroy()
                    self.refresh_balance()
                else:
                    messagebox.showerror("失败", "转账失败，请检查卡号和余额")
            except Exception as e:
                messagebox.showerror("错误", f"转账失败: {str(e)}")

        # 按钮
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20, fill=tk.X)

        ttk.Button(btn_frame, text="确认转账", command=do_transfer,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)

    def customer_check_balance(self):
        """查询余额"""
        try:
            balance = self.bank_system.card_service.check_balance(self.current_user['cardID'])
            if balance is not None:
                messagebox.showinfo("余额查询", f"当前余额: ¥{balance}")
                self.current_user['balance'] = balance
            else:
                messagebox.showerror("错误", "无法获取余额信息")
        except Exception as e:
            messagebox.showerror("错误", f"查询余额失败: {str(e)}")

    def customer_transaction_history(self):
        """查看交易记录"""
        try:
            transactions = self.bank_system.transaction_service.get_transactions(
                self.current_user['cardID'])
            self.show_transaction_table(transactions, "我的交易记录")
        except Exception as e:
            messagebox.showerror("错误", f"获取交易记录失败: {str(e)}")

    def customer_change_password(self):
        """修改密码"""
        # 创建密码修改对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("修改密码")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # 居中显示
        self.center_dialog(dialog)

        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="修改密码", style='Title.TLabel').pack(pady=(0, 20))

        # 新密码
        ttk.Label(form_frame, text="新密码(6位数字):", style='Heading.TLabel').pack(anchor=tk.W)
        new_pass_entry = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 11))
        new_pass_entry.pack(pady=(5, 10))

        # 确认密码
        ttk.Label(form_frame, text="确认密码:", style='Heading.TLabel').pack(anchor=tk.W)
        confirm_pass_entry = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 11))
        confirm_pass_entry.pack(pady=(5, 20))

        def do_change_password():
            new_pass = new_pass_entry.get().strip()
            confirm_pass = confirm_pass_entry.get().strip()

            if not new_pass or not confirm_pass:
                messagebox.showerror("错误", "请输入密码")
                return

            if new_pass != confirm_pass:
                messagebox.showerror("错误", "两次输入的密码不一致")
                return

            if len(new_pass) != 6 or not new_pass.isdigit():
                messagebox.showerror("错误", "密码必须为6位数字")
                return

            try:
                if self.bank_system.card_service.change_card_password(
                    self.current_user['cardID'], new_pass):
                    messagebox.showinfo("成功", "密码修改成功")
                    dialog.destroy()
                else:
                    messagebox.showerror("失败", "密码修改失败")
            except Exception as e:
                messagebox.showerror("错误", f"密码修改失败: {str(e)}")

        # 按钮
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20, fill=tk.X)

        ttk.Button(btn_frame, text="确认修改", command=do_change_password,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)

    def customer_report_loss(self):
        """银行卡挂失"""
        result = messagebox.askyesno("确认挂失", "确定要挂失这张银行卡吗？\n挂失后将无法继续使用该卡。")
        if result:
            try:
                if self.bank_system.card_service.report_loss(self.current_user['cardID']):
                    messagebox.showinfo("成功", "银行卡挂失成功")
                    self.logout()  # 挂失后自动退出登录
                else:
                    messagebox.showerror("失败", "挂失操作失败")
            except Exception as e:
                messagebox.showerror("错误", f"挂失失败: {str(e)}")

    def show_transaction_table(self, data, title):
        """显示交易记录表格"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        # 标题
        title_label = ttk.Label(self.work_frame, text=title, style='Heading.TLabel')
        title_label.pack(pady=(0, 10))

        if not data:
            no_data_label = ttk.Label(self.work_frame, text="暂无数据", style='Info.TLabel')
            no_data_label.pack()
            return

        # 创建表格框架
        table_frame = ttk.Frame(self.work_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建Treeview
        columns = list(data[0].keys()) if data else []
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        # 设置列标题
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        # 插入数据
        for row in data:
            values = [str(row[col]) if row[col] is not None else '' for col in columns]
            tree.insert('', tk.END, values=values)

        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=h_scrollbar.set)

        # 布局
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # 管理员功能实现
    def show_customer_management(self):
        """显示客户管理界面"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        # 标题和操作按钮
        header_frame = ttk.Frame(self.work_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="客户管理", style='Heading.TLabel').pack(side=tk.LEFT)

        # 操作按钮
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="添加客户", command=self.add_customer,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_customer_list,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="搜索客户", command=self.search_customer,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=2)

        # 显示客户列表
        self.refresh_customer_list()

    def refresh_customer_list(self):
        """刷新客户列表"""
        try:
            customers = self.bank_system.customer_service.get_customer_info()
            self.show_customer_table(customers)
        except Exception as e:
            messagebox.showerror("错误", f"获取客户列表失败: {str(e)}")

    def show_customer_table(self, customers):
        """显示客户表格"""
        # 清除现有表格
        for widget in self.work_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and widget != self.work_frame.winfo_children()[0]:
                widget.destroy()

        if not customers:
            no_data_label = ttk.Label(self.work_frame, text="暂无客户数据", style='Info.TLabel')
            no_data_label.pack(pady=20)
            return

        # 创建表格框架
        table_frame = ttk.Frame(self.work_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建Treeview
        columns = ('customerID', 'customerName', 'PID', 'telephone', 'address')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        # 设置列标题和宽度
        headers = {'customerID': '客户ID', 'customerName': '姓名', 'PID': '身份证号',
                  'telephone': '电话', 'address': '地址'}
        widths = {'customerID': 80, 'customerName': 100, 'PID': 150,
                 'telephone': 120, 'address': 200}

        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor=tk.CENTER)

        # 插入数据
        for customer in customers:
            values = [
                customer.get('customerID', ''),
                customer.get('customerName', ''),
                customer.get('PID', ''),
                customer.get('telephone', ''),
                customer.get('address', '') or '未填写'
            ]
            tree.insert('', tk.END, values=values)

        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)

        # 布局
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定双击事件
        tree.bind('<Double-1>', lambda e: self.edit_customer(tree))

        # 右键菜单
        def show_context_menu(event):
            item = tree.selection()[0] if tree.selection() else None
            if item:
                context_menu = tk.Menu(self.root, tearoff=0)
                context_menu.add_command(label="编辑客户",
                                       command=lambda: self.edit_customer(tree))
                context_menu.add_command(label="删除客户",
                                       command=lambda: self.delete_customer(tree))
                context_menu.add_command(label="查看银行卡",
                                       command=lambda: self.view_customer_cards(tree))
                context_menu.post(event.x_root, event.y_root)

        tree.bind('<Button-3>', show_context_menu)

    def run(self):
        """运行GUI应用"""
        self.root.mainloop()


# 将扩展功能混入主类
from BankSystemGUI_Extended import BankSystemGUIExtended

# 使用多重继承将扩展功能添加到主类
class BankSystemGUIComplete(BankSystemGUI, BankSystemGUIExtended):
    """完整的银行系统GUI类"""
    pass


def main():
    """主函数"""
    try:
        app = BankSystemGUIComplete()
        app.run()
    except Exception as e:
        print(f"应用启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
