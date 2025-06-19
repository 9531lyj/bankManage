#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行管理系统GUI界面扩展功能
包含管理员的各种管理功能实现
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime, date
import csv


class BankSystemGUIExtended:
    """银行系统GUI扩展功能类"""

    def center_dialog(self, dialog):
        """居中显示对话框"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def add_customer(self):
        """添加客户对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加客户")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)  # 允许调整大小
        
        # 居中显示
        self.center_dialog(dialog)

        # 表单框架
        form_frame = ttk.Frame(dialog, padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="添加客户", style='Title.TLabel').pack(pady=(0, 15))

        # 表单字段
        fields = {}

        # 姓名
        ttk.Label(form_frame, text="姓名*:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['name'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['name'].pack(pady=(3, 8), fill=tk.X)

        # 身份证号
        ttk.Label(form_frame, text="身份证号*:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['pid'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['pid'].pack(pady=(3, 8), fill=tk.X)

        # 电话
        ttk.Label(form_frame, text="电话*:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['telephone'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['telephone'].pack(pady=(3, 8), fill=tk.X)

        # 地址
        ttk.Label(form_frame, text="地址:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['address'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['address'].pack(pady=(3, 15), fill=tk.X)
        
        def do_add_customer():
            name = fields['name'].get().strip()
            pid = fields['pid'].get().strip()
            telephone = fields['telephone'].get().strip()
            address = fields['address'].get().strip() or None
            
            if not name or not pid or not telephone:
                messagebox.showerror("错误", "请填写所有必填字段（标*）")
                return
                
            try:
                # 先验证输入
                if len(pid) != 18:
                    messagebox.showerror("错误", "身份证号必须为18位")
                    return

                if len(telephone) != 11:
                    messagebox.showerror("错误", "电话号码必须为11位")
                    return

                # 尝试添加客户
                result = self.bank_system.customer_service.add_customer(name, pid, telephone, address)
                if result:
                    messagebox.showinfo("成功", "客户添加成功")
                    dialog.destroy()
                    self.refresh_customer_list()
                else:
                    messagebox.showerror("失败", "客户添加失败，可能是身份证号已存在")
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"添加客户错误详情: {error_details}")
                messagebox.showerror("错误", f"添加客户失败: {str(e)}\n\n详细错误信息已输出到控制台")
        
        # 按钮框架
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(btn_frame, text="添加", command=do_add_customer,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)
    
    def edit_customer(self, tree):
        """编辑客户信息"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要编辑的客户")
            return
            
        item = tree.item(selection[0])
        customer_id = item['values'][0]
        
        # 获取客户详细信息
        try:
            customer_info = self.bank_system.customer_service.get_customer_info(customer_id)
            if not customer_info:
                messagebox.showerror("错误", "无法获取客户信息")
                return
            customer = customer_info[0]
        except Exception as e:
            messagebox.showerror("错误", f"获取客户信息失败: {str(e)}")
            return
        
        # 创建编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑客户")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text=f"编辑客户 (ID: {customer_id})", style='Title.TLabel').pack(pady=(0, 20))
        
        # 表单字段
        fields = {}
        
        # 姓名
        ttk.Label(form_frame, text="姓名:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['name'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['name'].pack(pady=(5, 10), fill=tk.X)
        fields['name'].insert(0, customer['customerName'])
        
        # 电话
        ttk.Label(form_frame, text="电话:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['telephone'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['telephone'].pack(pady=(5, 10), fill=tk.X)
        fields['telephone'].insert(0, customer['telephone'])
        
        # 地址
        ttk.Label(form_frame, text="地址:", style='Heading.TLabel').pack(anchor=tk.W)
        fields['address'] = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        fields['address'].pack(pady=(5, 20), fill=tk.X)
        fields['address'].insert(0, customer['address'] or '')
        
        def do_update_customer():
            name = fields['name'].get().strip()
            telephone = fields['telephone'].get().strip()
            address = fields['address'].get().strip() or None
            
            if not name or not telephone:
                messagebox.showerror("错误", "姓名和电话不能为空")
                return
                
            try:
                if self.bank_system.customer_service.update_customer(
                    customer_id, name, telephone, address):
                    messagebox.showinfo("成功", "客户信息更新成功")
                    dialog.destroy()
                    self.refresh_customer_list()
                else:
                    messagebox.showerror("失败", "客户信息更新失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新客户信息失败: {str(e)}")
        
        # 按钮
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20, fill=tk.X)

        ttk.Button(btn_frame, text="更新", command=do_update_customer,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)
    
    def delete_customer(self, tree):
        """删除客户"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要删除的客户")
            return
            
        item = tree.item(selection[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]
        
        result = messagebox.askyesno("确认删除", 
                                   f"确定要删除客户 {customer_name} (ID: {customer_id}) 吗？\n此操作不可撤销！")
        if result:
            try:
                if self.bank_system.customer_service.delete_customer(customer_id):
                    messagebox.showinfo("成功", "客户删除成功")
                    self.refresh_customer_list()
                else:
                    messagebox.showerror("失败", "客户删除失败")
            except Exception as e:
                messagebox.showerror("错误", f"删除客户失败: {str(e)}")
    
    def search_customer(self):
        """搜索客户"""
        keyword = simpledialog.askstring("搜索客户", "请输入搜索关键词（姓名、电话或身份证号）:")
        if keyword:
            try:
                customers = self.bank_system.customer_service.search_customers(keyword)
                self.show_customer_table(customers)
                if not customers:
                    messagebox.showinfo("搜索结果", "未找到匹配的客户")
            except Exception as e:
                messagebox.showerror("错误", f"搜索失败: {str(e)}")
    
    def view_customer_cards(self, tree):
        """查看客户的银行卡"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择客户")
            return
            
        item = tree.item(selection[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]
        
        try:
            cards = self.bank_system.card_service.get_card_info(customer_id=customer_id)
            
            # 创建新窗口显示银行卡信息
            card_window = tk.Toplevel(self.root)
            card_window.title(f"{customer_name} 的银行卡")
            card_window.geometry("800x400")
            card_window.transient(self.root)
            
            if not cards:
                ttk.Label(card_window, text="该客户暂无银行卡", 
                         style='Info.TLabel').pack(expand=True)
                return
            
            # 创建表格显示银行卡信息
            frame = ttk.Frame(card_window, padding=10)
            frame.pack(fill=tk.BOTH, expand=True)
            
            columns = ('cardID', 'curID', 'balance', 'openDate', 'IsReportLoss')
            tree_cards = ttk.Treeview(frame, columns=columns, show='headings')
            
            headers = {'cardID': '卡号', 'curID': '货币', 'balance': '余额', 
                      'openDate': '开户日期', 'IsReportLoss': '挂失状态'}
            
            for col in columns:
                tree_cards.heading(col, text=headers[col])
                tree_cards.column(col, width=120, anchor=tk.CENTER)
            
            for card in cards:
                values = [
                    card.get('cardID', ''),
                    card.get('curID', ''),
                    f"¥{card.get('balance', 0)}",
                    str(card.get('openDate', '')),
                    card.get('IsReportLoss', '')
                ]
                tree_cards.insert('', tk.END, values=values)
            
            tree_cards.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取银行卡信息失败: {str(e)}")
    
    def show_card_management(self):
        """显示银行卡管理界面"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()
            
        # 标题和操作按钮
        header_frame = ttk.Frame(self.work_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="银行卡管理", style='Heading.TLabel').pack(side=tk.LEFT)
        
        # 操作按钮
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="添加银行卡", command=self.add_card, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_card_list, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=2)
        
        # 显示银行卡列表
        self.refresh_card_list()
    
    def refresh_card_list(self):
        """刷新银行卡列表"""
        try:
            cards = self.bank_system.card_service.get_card_info()
            self.show_card_table(cards)
        except Exception as e:
            messagebox.showerror("错误", f"获取银行卡列表失败: {str(e)}")
    
    def show_card_table(self, cards):
        """显示银行卡表格"""
        # 清除现有表格
        for widget in self.work_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and widget != self.work_frame.winfo_children()[0]:
                widget.destroy()
        
        if not cards:
            no_data_label = ttk.Label(self.work_frame, text="暂无银行卡数据", style='Info.TLabel')
            no_data_label.pack(pady=20)
            return
            
        # 创建表格框架
        table_frame = ttk.Frame(self.work_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建Treeview
        columns = ('cardID', 'customerName', 'curID', 'balance', 'openDate', 'IsReportLoss')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # 设置列标题和宽度
        headers = {'cardID': '卡号', 'customerName': '客户姓名', 'curID': '货币', 
                  'balance': '余额', 'openDate': '开户日期', 'IsReportLoss': '挂失状态'}
        widths = {'cardID': 150, 'customerName': 100, 'curID': 80, 
                 'balance': 100, 'openDate': 120, 'IsReportLoss': 80}
        
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor=tk.CENTER)
        
        # 插入数据
        for card in cards:
            values = [
                card.get('cardID', ''),
                card.get('customerName', ''),
                card.get('curID', ''),
                f"¥{card.get('balance', 0)}",
                str(card.get('openDate', '')),
                card.get('IsReportLoss', '')
            ]
            tree.insert('', tk.END, values=values)
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)
        
        # 布局
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右键菜单
        def show_context_menu(event):
            item = tree.selection()[0] if tree.selection() else None
            if item:
                context_menu = tk.Menu(self.root, tearoff=0)
                context_menu.add_command(label="编辑银行卡", 
                                       command=lambda: self.edit_card(tree))
                context_menu.add_command(label="删除银行卡", 
                                       command=lambda: self.delete_card(tree))
                context_menu.add_command(label="挂失/解挂", 
                                       command=lambda: self.toggle_card_loss(tree))
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind('<Button-3>', show_context_menu)

    def add_card(self):
        """添加银行卡"""
        # 首先获取客户列表
        try:
            customers = self.bank_system.customer_service.get_customer_info()
            if not customers:
                messagebox.showerror("错误", "系统中没有客户，请先添加客户")
                return
        except Exception as e:
            messagebox.showerror("错误", f"获取客户列表失败: {str(e)}")
            return

        # 获取存款类型列表
        try:
            deposit_types = self.bank_system.deposit_service.get_deposit_types()
            if not deposit_types:
                messagebox.showerror("错误", "系统中没有存款类型，请先添加存款类型")
                return
        except Exception as e:
            messagebox.showerror("错误", f"获取存款类型失败: {str(e)}")
            return

        # 创建添加银行卡对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加银行卡")
        dialog.geometry("550x600")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)  # 允许调整大小

        form_frame = ttk.Frame(dialog, padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="添加银行卡", style='Title.TLabel').pack(pady=(0, 15))

        # 卡号
        ttk.Label(form_frame, text="银行卡号*:", style='Heading.TLabel').pack(anchor=tk.W)
        card_id_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        card_id_entry.pack(pady=(3, 6), fill=tk.X)

        # 客户选择
        ttk.Label(form_frame, text="选择客户*:", style='Heading.TLabel').pack(anchor=tk.W)
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(form_frame, textvariable=customer_var,
                                     width=30, font=('Arial', 11), state='readonly')
        customer_options = [f"{c['customerID']} - {c['customerName']}" for c in customers]
        customer_combo['values'] = customer_options
        customer_combo.pack(pady=(3, 6), fill=tk.X)

        # 存款类型选择
        ttk.Label(form_frame, text="存款类型*:", style='Heading.TLabel').pack(anchor=tk.W)
        deposit_var = tk.StringVar()
        deposit_combo = ttk.Combobox(form_frame, textvariable=deposit_var,
                                   width=30, font=('Arial', 11), state='readonly')
        deposit_options = [f"{d['savingID']} - {d['savingName']}" for d in deposit_types]
        deposit_combo['values'] = deposit_options
        deposit_combo.pack(pady=(3, 6), fill=tk.X)

        # 开户金额
        ttk.Label(form_frame, text="开户金额*:", style='Heading.TLabel').pack(anchor=tk.W)
        open_money_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        open_money_entry.pack(pady=(3, 6), fill=tk.X)
        open_money_entry.insert(0, "0")

        # 初始余额
        ttk.Label(form_frame, text="初始余额*:", style='Heading.TLabel').pack(anchor=tk.W)
        balance_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        balance_entry.pack(pady=(3, 6), fill=tk.X)
        balance_entry.insert(0, "0")

        # 密码
        ttk.Label(form_frame, text="密码(6位数字):", style='Heading.TLabel').pack(anchor=tk.W)
        password_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11), show="*")
        password_entry.pack(pady=(3, 12), fill=tk.X)
        password_entry.insert(0, "888888")

        def do_add_card():
            card_id = card_id_entry.get().strip()
            customer_selection = customer_var.get()
            deposit_selection = deposit_var.get()
            password = password_entry.get().strip()

            try:
                open_money = float(open_money_entry.get().strip())
                balance = float(balance_entry.get().strip())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的金额")
                return

            if not card_id or not customer_selection or not deposit_selection:
                messagebox.showerror("错误", "请填写所有必填字段")
                return

            if len(password) != 6 or not password.isdigit():
                messagebox.showerror("错误", "密码必须为6位数字")
                return

            # 提取ID
            customer_id = customer_selection.split(' - ')[0]
            saving_id = deposit_selection.split(' - ')[0]

            try:
                if self.bank_system.card_service.add_card(
                    card_id, saving_id, open_money, balance, customer_id, password):
                    messagebox.showinfo("成功", "银行卡添加成功")
                    dialog.destroy()
                    self.refresh_card_list()
                else:
                    messagebox.showerror("失败", "银行卡添加失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加银行卡失败: {str(e)}")

        # 按钮
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="添加", command=do_add_card,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)

    def edit_card(self, tree):
        """编辑银行卡信息"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要编辑的银行卡")
            return

        item = tree.item(selection[0])
        card_id = item['values'][0]

        # 获取银行卡详细信息
        try:
            card_info = self.bank_system.card_service.get_card_info(card_id=card_id)
            if not card_info:
                messagebox.showerror("错误", "无法获取银行卡信息")
                return
            card = card_info[0]
        except Exception as e:
            messagebox.showerror("错误", f"获取银行卡信息失败: {str(e)}")
            return

        # 创建编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑银行卡")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text=f"编辑银行卡 ({card_id})", style='Title.TLabel').pack(pady=(0, 20))

        # 余额
        ttk.Label(form_frame, text="余额:", style='Heading.TLabel').pack(anchor=tk.W)
        balance_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        balance_entry.pack(pady=(5, 20), fill=tk.X)
        balance_entry.insert(0, str(card['balance']))

        def do_update_card():
            try:
                balance = float(balance_entry.get().strip())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的余额")
                return

            try:
                if self.bank_system.card_service.update_card_info(card_id, balance=balance):
                    messagebox.showinfo("成功", "银行卡信息更新成功")
                    dialog.destroy()
                    self.refresh_card_list()
                else:
                    messagebox.showerror("失败", "银行卡信息更新失败")
            except Exception as e:
                messagebox.showerror("错误", f"更新银行卡信息失败: {str(e)}")

        # 按钮
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20, fill=tk.X)

        ttk.Button(btn_frame, text="更新", command=do_update_card,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)

    def delete_card(self, tree):
        """删除银行卡"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要删除的银行卡")
            return

        item = tree.item(selection[0])
        card_id = item['values'][0]

        result = messagebox.askyesno("确认删除",
                                   f"确定要删除银行卡 {card_id} 吗？\n此操作不可撤销！")
        if result:
            try:
                if self.bank_system.card_service.delete_card(card_id):
                    messagebox.showinfo("成功", "银行卡删除成功")
                    self.refresh_card_list()
                else:
                    messagebox.showerror("失败", "银行卡删除失败")
            except Exception as e:
                messagebox.showerror("错误", f"删除银行卡失败: {str(e)}")

    def toggle_card_loss(self, tree):
        """挂失/解挂银行卡"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择银行卡")
            return

        item = tree.item(selection[0])
        card_id = item['values'][0]
        current_status = item['values'][5]

        if current_status == '是':
            action = "解除挂失"
            new_status = '否'
        else:
            action = "挂失"
            new_status = '是'

        result = messagebox.askyesno("确认操作", f"确定要{action}银行卡 {card_id} 吗？")
        if result:
            try:
                # 这里需要在CardService中添加解挂功能
                if current_status == '否':  # 当前未挂失，执行挂失
                    if self.bank_system.card_service.report_loss(card_id):
                        messagebox.showinfo("成功", "银行卡挂失成功")
                        self.refresh_card_list()
                    else:
                        messagebox.showerror("失败", "挂失操作失败")
                else:  # 当前已挂失，执行解挂（需要添加此功能）
                    messagebox.showinfo("提示", "解挂功能需要在CardService中实现")
            except Exception as e:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

    def show_deposit_management(self):
        """显示存款类型管理界面"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        # 标题和操作按钮
        header_frame = ttk.Frame(self.work_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="存款类型管理", style='Heading.TLabel').pack(side=tk.LEFT)

        # 操作按钮
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="添加存款类型", command=self.add_deposit_type,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_deposit_list,
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=2)

        # 显示存款类型列表
        self.refresh_deposit_list()

    def refresh_deposit_list(self):
        """刷新存款类型列表"""
        try:
            deposits = self.bank_system.deposit_service.get_deposit_types()
            self.show_deposit_table(deposits)
        except Exception as e:
            messagebox.showerror("错误", f"获取存款类型列表失败: {str(e)}")

    def show_deposit_table(self, deposits):
        """显示存款类型表格"""
        # 清除现有表格
        for widget in self.work_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and widget != self.work_frame.winfo_children()[0]:
                widget.destroy()

        if not deposits:
            no_data_label = ttk.Label(self.work_frame, text="暂无存款类型数据", style='Info.TLabel')
            no_data_label.pack(pady=20)
            return

        # 创建表格框架
        table_frame = ttk.Frame(self.work_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建Treeview
        columns = ('savingID', 'savingName', 'descrip', 'term')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        # 设置列标题和宽度
        headers = {'savingID': 'ID', 'savingName': '存款类型', 'descrip': '描述', 'term': '期限'}
        widths = {'savingID': 80, 'savingName': 150, 'descrip': 300, 'term': 100}

        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor=tk.CENTER)

        # 插入数据
        for deposit in deposits:
            values = [
                deposit.get('savingID', ''),
                deposit.get('savingName', ''),
                deposit.get('descrip', ''),
                deposit.get('term', '') or '无期限'
            ]
            tree.insert('', tk.END, values=values)

        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)

        # 布局
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 右键菜单
        def show_context_menu(event):
            item = tree.selection()[0] if tree.selection() else None
            if item:
                context_menu = tk.Menu(self.root, tearoff=0)
                context_menu.add_command(label="编辑存款类型",
                                       command=lambda: self.edit_deposit_type(tree))
                context_menu.add_command(label="删除存款类型",
                                       command=lambda: self.delete_deposit_type(tree))
                context_menu.post(event.x_root, event.y_root)

        tree.bind('<Button-3>', show_context_menu)

    def add_deposit_type(self):
        """添加存款类型"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加存款类型")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="添加存款类型", style='Title.TLabel').pack(pady=(0, 20))

        # 存款类型名称
        ttk.Label(form_frame, text="存款类型名称*:", style='Heading.TLabel').pack(anchor=tk.W)
        name_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        name_entry.pack(pady=(5, 10), fill=tk.X)

        # 描述
        ttk.Label(form_frame, text="描述*:", style='Heading.TLabel').pack(anchor=tk.W)
        desc_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        desc_entry.pack(pady=(5, 10), fill=tk.X)

        # 期限
        ttk.Label(form_frame, text="期限(可选):", style='Heading.TLabel').pack(anchor=tk.W)
        term_entry = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        term_entry.pack(pady=(5, 20), fill=tk.X)

        def do_add_deposit():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            term = term_entry.get().strip() or None

            if not name or not desc:
                messagebox.showerror("错误", "请填写存款类型名称和描述")
                return

            try:
                if self.bank_system.deposit_service.add_deposit_type(name, desc, term):
                    messagebox.showinfo("成功", "存款类型添加成功")
                    dialog.destroy()
                    self.refresh_deposit_list()
                else:
                    messagebox.showerror("失败", "存款类型添加失败")
            except Exception as e:
                messagebox.showerror("错误", f"添加存款类型失败: {str(e)}")

        # 按钮
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20, fill=tk.X)

        ttk.Button(btn_frame, text="添加", command=do_add_deposit,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="取消", command=dialog.destroy,
                  style='Secondary.TButton').pack(side=tk.LEFT)

    def show_transaction_query(self):
        """显示交易记录查询界面"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        # 标题
        ttk.Label(self.work_frame, text="交易记录查询", style='Heading.TLabel').pack(pady=(0, 20))

        # 查询条件框架
        query_frame = ttk.LabelFrame(self.work_frame, text="查询条件", padding=10)
        query_frame.pack(fill=tk.X, pady=(0, 10))

        # 第一行：卡号和日期范围
        row1 = ttk.Frame(query_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Label(row1, text="银行卡号:").pack(side=tk.LEFT)
        card_id_entry = ttk.Entry(row1, width=20)
        card_id_entry.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(row1, text="开始日期:").pack(side=tk.LEFT)
        start_date_entry = ttk.Entry(row1, width=12)
        start_date_entry.pack(side=tk.LEFT, padx=(5, 20))
        start_date_entry.insert(0, "2024-01-01")

        ttk.Label(row1, text="结束日期:").pack(side=tk.LEFT)
        end_date_entry = ttk.Entry(row1, width=12)
        end_date_entry.pack(side=tk.LEFT, padx=(5, 20))
        end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # 查询按钮
        def do_query():
            card_id = card_id_entry.get().strip() or None
            start_date = start_date_entry.get().strip() or None
            end_date = end_date_entry.get().strip() or None

            try:
                transactions = self.bank_system.transaction_service.get_transactions(
                    card_id, start_date, end_date)
                self.show_transaction_result_table(transactions)
            except Exception as e:
                messagebox.showerror("错误", f"查询交易记录失败: {str(e)}")

        ttk.Button(row1, text="查询", command=do_query,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(20, 0))

        # 结果显示区域
        self.transaction_result_frame = ttk.Frame(self.work_frame)
        self.transaction_result_frame.pack(fill=tk.BOTH, expand=True)

        # 默认显示所有交易记录
        try:
            all_transactions = self.bank_system.transaction_service.get_transactions()
            self.show_transaction_result_table(all_transactions)
        except Exception as e:
            ttk.Label(self.transaction_result_frame,
                     text=f"加载交易记录失败: {str(e)}",
                     style='Error.TLabel').pack(pady=20)

    def show_transaction_result_table(self, transactions):
        """显示交易记录结果表格"""
        # 清除现有结果
        for widget in self.transaction_result_frame.winfo_children():
            widget.destroy()

        if not transactions:
            ttk.Label(self.transaction_result_frame, text="未找到交易记录",
                     style='Info.TLabel').pack(pady=20)
            return

        # 创建表格
        columns = ('tradeID', 'cardID', 'tradeDate', 'tradeMoney', 'tradeType', 'remark')
        tree = ttk.Treeview(self.transaction_result_frame, columns=columns,
                           show='headings', height=15)

        # 设置列标题
        headers = {'tradeID': '交易ID', 'cardID': '银行卡号', 'tradeDate': '交易日期',
                  'tradeMoney': '交易金额', 'tradeType': '交易类型', 'remark': '备注'}
        widths = {'tradeID': 80, 'cardID': 150, 'tradeDate': 120,
                 'tradeMoney': 100, 'tradeType': 80, 'remark': 200}

        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor=tk.CENTER)

        # 插入数据
        for transaction in transactions:
            values = [
                transaction.get('tradeID', ''),
                transaction.get('cardID', ''),
                str(transaction.get('tradeDate', '')),
                f"¥{transaction.get('tradeMoney', 0)}",
                transaction.get('tradeType', ''),
                transaction.get('remark', '') or ''
            ]
            tree.insert('', tk.END, values=values)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.transaction_result_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # 布局
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_report_management(self):
        """显示报表管理界面"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        # 标题
        ttk.Label(self.work_frame, text="报表管理", style='Heading.TLabel').pack(pady=(0, 20))

        # 报表类型选择
        report_frame = ttk.LabelFrame(self.work_frame, text="生成报表", padding=20)
        report_frame.pack(fill=tk.X, pady=(0, 20))

        # 报表类型
        ttk.Label(report_frame, text="报表类型:", style='Heading.TLabel').pack(anchor=tk.W)
        report_type_var = tk.StringVar(value="交易明细")
        report_types = ["交易明细", "月度汇总", "年度汇总", "账户统计"]
        report_combo = ttk.Combobox(report_frame, textvariable=report_type_var,
                                   values=report_types, state='readonly', width=20)
        report_combo.pack(anchor=tk.W, pady=(5, 10))

        # 日期范围
        date_frame = ttk.Frame(report_frame)
        date_frame.pack(fill=tk.X, pady=10)

        ttk.Label(date_frame, text="开始日期:").pack(side=tk.LEFT)
        start_date_entry = ttk.Entry(date_frame, width=12)
        start_date_entry.pack(side=tk.LEFT, padx=(5, 20))
        start_date_entry.insert(0, "2024-01-01")

        ttk.Label(date_frame, text="结束日期:").pack(side=tk.LEFT)
        end_date_entry = ttk.Entry(date_frame, width=12)
        end_date_entry.pack(side=tk.LEFT, padx=(5, 20))
        end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # 可选参数
        optional_frame = ttk.Frame(report_frame)
        optional_frame.pack(fill=tk.X, pady=10)

        ttk.Label(optional_frame, text="银行卡号(可选):").pack(side=tk.LEFT)
        card_id_entry = ttk.Entry(optional_frame, width=20)
        card_id_entry.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(optional_frame, text="客户ID(可选):").pack(side=tk.LEFT)
        customer_id_entry = ttk.Entry(optional_frame, width=10)
        customer_id_entry.pack(side=tk.LEFT, padx=(5, 20))

        def generate_report():
            report_type = report_type_var.get()
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            card_id = card_id_entry.get().strip() or None
            customer_id = customer_id_entry.get().strip() or None

            if not start_date or not end_date:
                messagebox.showerror("错误", "请输入开始日期和结束日期")
                return

            try:
                # 转换客户ID为整数
                if customer_id:
                    customer_id = int(customer_id)

                success = self.bank_system.report_service.generate_report(
                    report_type, start_date, end_date, card_id, customer_id)

                if success:
                    messagebox.showinfo("成功", f"{report_type}报表生成成功！\n文件已保存到当前目录")
                else:
                    messagebox.showerror("失败", "报表生成失败")

            except ValueError:
                messagebox.showerror("错误", "客户ID必须是数字")
            except Exception as e:
                messagebox.showerror("错误", f"生成报表失败: {str(e)}")

        ttk.Button(report_frame, text="生成报表", command=generate_report,
                  style='Primary.TButton').pack(pady=20)

        # 快速报表按钮
        quick_frame = ttk.LabelFrame(self.work_frame, text="快速报表", padding=20)
        quick_frame.pack(fill=tk.X)

        quick_buttons = [
            ("今日交易报表", lambda: self.quick_report("today")),
            ("本月交易报表", lambda: self.quick_report("month")),
            ("本年交易报表", lambda: self.quick_report("year")),
            ("导出所有客户", lambda: self.export_all_customers()),
            ("导出所有银行卡", lambda: self.export_all_cards())
        ]

        for i, (text, command) in enumerate(quick_buttons):
            btn = ttk.Button(quick_frame, text=text, command=command,
                           style='Secondary.TButton', width=15)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)

    def quick_report(self, period):
        """快速生成报表"""
        today = datetime.now()

        if period == "today":
            start_date = end_date = today.strftime("%Y-%m-%d")
            report_type = "交易明细"
        elif period == "month":
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
            report_type = "月度汇总"
        elif period == "year":
            start_date = today.replace(month=1, day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
            report_type = "年度汇总"

        try:
            success = self.bank_system.report_service.generate_report(
                report_type, start_date, end_date)

            if success:
                messagebox.showinfo("成功", f"{report_type}报表生成成功！")
            else:
                messagebox.showerror("失败", "报表生成失败")
        except Exception as e:
            messagebox.showerror("错误", f"生成报表失败: {str(e)}")

    def export_all_customers(self):
        """导出所有客户信息"""
        try:
            customers = self.bank_system.customer_service.get_customer_info()
            if customers:
                filename = f"all_customers_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                if self.bank_system.customer_service.export_to_csv(customers, filename):
                    messagebox.showinfo("成功", f"客户信息已导出到 {filename}")
                else:
                    messagebox.showerror("失败", "导出失败")
            else:
                messagebox.showinfo("提示", "没有客户数据可导出")
        except Exception as e:
            messagebox.showerror("错误", f"导出客户信息失败: {str(e)}")

    def export_all_cards(self):
        """导出所有银行卡信息"""
        try:
            cards = self.bank_system.card_service.get_card_info()
            if cards:
                filename = f"all_cards_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                if self.bank_system.card_service.export_to_csv(cards, filename):
                    messagebox.showinfo("成功", f"银行卡信息已导出到 {filename}")
                else:
                    messagebox.showerror("失败", "导出失败")
            else:
                messagebox.showinfo("提示", "没有银行卡数据可导出")
        except Exception as e:
            messagebox.showerror("错误", f"导出银行卡信息失败: {str(e)}")

    def show_system_statistics(self):
        """显示系统统计信息"""
        for widget in self.work_frame.winfo_children():
            widget.destroy()

        # 标题
        ttk.Label(self.work_frame, text="系统统计", style='Heading.TLabel').pack(pady=(0, 20))

        try:
            # 获取统计数据
            customers = self.bank_system.customer_service.get_customer_info()
            cards = self.bank_system.card_service.get_card_info()
            transactions = self.bank_system.transaction_service.get_transactions()
            deposits = self.bank_system.deposit_service.get_deposit_types()

            # 计算统计信息
            total_customers = len(customers) if customers else 0
            total_cards = len(cards) if cards else 0
            total_transactions = len(transactions) if transactions else 0
            total_deposits = len(deposits) if deposits else 0

            # 计算总余额
            total_balance = sum(card.get('balance', 0) for card in cards) if cards else 0

            # 计算今日交易
            today = datetime.now().strftime("%Y-%m-%d")
            today_transactions = [t for t in transactions
                                if str(t.get('tradeDate', '')).startswith(today)] if transactions else []
            today_transaction_count = len(today_transactions)
            today_transaction_amount = sum(t.get('tradeMoney', 0) for t in today_transactions)

            # 创建统计信息显示
            stats_frame = ttk.Frame(self.work_frame)
            stats_frame.pack(fill=tk.BOTH, expand=True, padx=20)

            # 基础统计
            basic_frame = ttk.LabelFrame(stats_frame, text="基础统计", padding=20)
            basic_frame.pack(fill=tk.X, pady=(0, 20))

            basic_stats = [
                ("客户总数", total_customers),
                ("银行卡总数", total_cards),
                ("存款类型数", total_deposits),
                ("交易记录总数", total_transactions),
                ("系统总余额", f"¥{total_balance:,.2f}")
            ]

            for i, (label, value) in enumerate(basic_stats):
                row = i // 2
                col = i % 2

                stat_frame = ttk.Frame(basic_frame)
                stat_frame.grid(row=row, column=col, padx=20, pady=10, sticky='w')

                ttk.Label(stat_frame, text=f"{label}:", style='Heading.TLabel').pack(anchor=tk.W)
                ttk.Label(stat_frame, text=str(value), style='Info.TLabel',
                         font=('Arial', 12, 'bold')).pack(anchor=tk.W)

            # 今日统计
            today_frame = ttk.LabelFrame(stats_frame, text="今日统计", padding=20)
            today_frame.pack(fill=tk.X, pady=(0, 20))

            today_stats = [
                ("今日交易笔数", today_transaction_count),
                ("今日交易金额", f"¥{today_transaction_amount:,.2f}")
            ]

            for i, (label, value) in enumerate(today_stats):
                stat_frame = ttk.Frame(today_frame)
                stat_frame.grid(row=0, column=i, padx=20, pady=10, sticky='w')

                ttk.Label(stat_frame, text=f"{label}:", style='Heading.TLabel').pack(anchor=tk.W)
                ttk.Label(stat_frame, text=str(value), style='Success.TLabel',
                         font=('Arial', 12, 'bold')).pack(anchor=tk.W)

            # 刷新按钮
            ttk.Button(stats_frame, text="刷新统计", command=self.show_system_statistics,
                      style='Primary.TButton').pack(pady=20)

        except Exception as e:
            error_label = ttk.Label(self.work_frame,
                                   text=f"获取统计信息失败: {str(e)}",
                                   style='Error.TLabel')
            error_label.pack(pady=20)
