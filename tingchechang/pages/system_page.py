import customtkinter as ctk
import os
import shutil
from datetime import datetime
from components.dialogs import MessageDialog, ConfirmDialog
from config import BACKUP_DIR

class SystemPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_update_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_update = on_update_callback
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        self.backup_frame = ctk.CTkFrame(self)
        self.backup_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        
        self.backup_label = ctk.CTkLabel(self.backup_frame, text='数据备份管理', font=('微软雅黑', 14, 'bold'))
        self.backup_label.grid(row=0, column=0, padx=15, pady=15, sticky='w')
        
        self.backup_btn = ctk.CTkButton(self.backup_frame, text='创建备份', command=self.on_backup,
                                        width=150, font=('微软雅黑', 14))
        self.backup_btn.grid(row=1, column=0, padx=15, pady=10, sticky='w')
        
        self.restore_btn = ctk.CTkButton(self.backup_frame, text='恢复备份', command=self.on_restore,
                                         width=150, font=('微软雅黑', 14))
        self.restore_btn.grid(row=2, column=0, padx=15, pady=10, sticky='w')
        
        self.backup_list_label = ctk.CTkLabel(self.backup_frame, text='备份文件列表:', font=('微软雅黑', 12))
        self.backup_list_label.grid(row=3, column=0, padx=15, pady=10, sticky='w')
        
        self.backup_listbox = ctk.CTkTextbox(self.backup_frame, height=150, font=('微软雅黑', 12))
        self.backup_listbox.grid(row=4, column=0, padx=15, pady=10, sticky='ew')
        
        self.delete_backup_btn = ctk.CTkButton(self.backup_frame, text='删除选中备份', command=self.on_delete_backup,
                                               width=150, font=('微软雅黑', 12), state='disabled')
        self.delete_backup_btn.grid(row=5, column=0, padx=15, pady=10, sticky='w')
        
        self.backup_listbox.bind('<<Modified>>', self.on_backup_list_select)
        
        self.refresh_backup_list()
    
    def refresh_backup_list(self):
        self.backup_listbox.delete('0.0', 'end')
        if os.path.exists(BACKUP_DIR):
            backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith('.sql')], reverse=True)
            for backup in backups:
                self.backup_listbox.insert('end', backup + '\n')
    
    def on_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(BACKUP_DIR, f'backup_{timestamp}.sql')
        
        try:
            self.db_manager.backup_database(backup_path)
            MessageDialog(self, '提示', '数据备份成功')
            self.refresh_backup_list()
        except Exception as e:
            MessageDialog(self, '错误', f'备份失败: {str(e)}')
    
    def on_restore(self):
        backup_text = self.backup_listbox.get('sel.first', 'sel.last').strip()
        if not backup_text:
            MessageDialog(self, '提示', '请先选择要恢复的备份文件')
            return
        
        confirm = ConfirmDialog(self, '确认恢复', 
                               f'确定要恢复备份文件 "{backup_text}" 吗？\n此操作将覆盖当前数据！')
        self.wait_window(confirm)
        
        if confirm.result:
            backup_path = os.path.join(BACKUP_DIR, backup_text)
            try:
                self.db_manager.restore_database(backup_path)
                MessageDialog(self, '提示', '数据恢复成功')
                self.on_update()
            except Exception as e:
                MessageDialog(self, '错误', f'恢复失败: {str(e)}')
    
    def on_delete_backup(self):
        backup_text = self.backup_listbox.get('sel.first', 'sel.last').strip()
        if not backup_text:
            return
        
        confirm = ConfirmDialog(self, '确认删除', f'确定要删除备份文件 "{backup_text}" 吗？')
        self.wait_window(confirm)
        
        if confirm.result:
            backup_path = os.path.join(BACKUP_DIR, backup_text)
            try:
                os.remove(backup_path)
                MessageDialog(self, '提示', '备份文件删除成功')
                self.refresh_backup_list()
            except Exception as e:
                MessageDialog(self, '错误', f'删除失败: {str(e)}')
    
    def on_backup_list_select(self, event):
        self.backup_listbox.edit_modified(False)
        try:
            self.backup_listbox.get('sel.first', 'sel.last')
            self.delete_backup_btn.configure(state='normal')
        except:
            self.delete_backup_btn.configure(state='disabled')
    
    def refresh(self):
        self.refresh_backup_list()