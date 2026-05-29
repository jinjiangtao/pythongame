import customtkinter as ctk
from tkinter import ttk
from utils.calculator import FeeCalculator
from components.dialogs import MessageDialog, ConfirmDialog
import csv
import os

class QueryPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_update_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_update = on_update_callback
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1
        self.filter_params = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=0, column=0, padx=20, pady=10, sticky='ew')
        self.filter_frame.grid_columnconfigure(0, weight=0)
        self.filter_frame.grid_columnconfigure(1, weight=1)
        self.filter_frame.grid_columnconfigure(2, weight=0)
        self.filter_frame.grid_columnconfigure(3, weight=1)
        self.filter_frame.grid_columnconfigure(4, weight=0)
        self.filter_frame.grid_columnconfigure(5, weight=1)
        self.filter_frame.grid_columnconfigure(6, weight=0)
        
        self.plate_label = ctk.CTkLabel(self.filter_frame, text='车牌号:', font=('微软雅黑', 12))
        self.plate_label.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        self.plate_entry = ctk.CTkEntry(self.filter_frame, width=120, font=('微软雅黑', 12))
        self.plate_entry.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        self.type_label = ctk.CTkLabel(self.filter_frame, text='车辆类型:', font=('微软雅黑', 12))
        self.type_label.grid(row=0, column=2, padx=5, pady=10, sticky='w')
        self.type_var = ctk.StringVar(value='全部')
        self.type_combo = ctk.CTkComboBox(self.filter_frame, variable=self.type_var,
                                          values=['全部', '小型车', '大型车', '新能源车'],
                                          width=120, font=('微软雅黑', 12))
        self.type_combo.grid(row=0, column=3, padx=5, pady=10, sticky='w')
        
        self.search_btn = ctk.CTkButton(self.filter_frame, text='查询', command=self.on_search,
                                        width=80, font=('微软雅黑', 12))
        self.search_btn.grid(row=0, column=4, padx=5, pady=10)
        
        self.export_btn = ctk.CTkButton(self.filter_frame, text='导出记录', command=self.on_export,
                                        width=80, font=('微软雅黑', 12))
        self.export_btn.grid(row=0, column=5, padx=5, pady=10)
        
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(self.table_frame, columns=('id', 'plate', 'type', 'area', 'entry', 'exit', 'duration', 'fee'),
                                show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('plate', text='车牌号')
        self.tree.heading('type', text='车辆类型')
        self.tree.heading('area', text='停放区域')
        self.tree.heading('entry', text='入场时间')
        self.tree.heading('exit', text='出场时间')
        self.tree.heading('duration', text='停放时长')
        self.tree.heading('fee', text='费用(元)')
        
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('plate', width=100, anchor='center')
        self.tree.column('type', width=80, anchor='center')
        self.tree.column('area', width=80, anchor='center')
        self.tree.column('entry', width=140, anchor='center')
        self.tree.column('exit', width=140, anchor='center')
        self.tree.column('duration', width=100, anchor='center')
        self.tree.column('fee', width=80, anchor='center')
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.pagination_frame = ctk.CTkFrame(self)
        self.pagination_frame.grid(row=2, column=0, padx=20, pady=10, sticky='ew')
        self.pagination_frame.grid_columnconfigure(0, weight=1)
        self.pagination_frame.grid_columnconfigure(1, weight=0)
        self.pagination_frame.grid_columnconfigure(2, weight=0)
        self.pagination_frame.grid_columnconfigure(3, weight=0)
        self.pagination_frame.grid_columnconfigure(4, weight=0)
        self.pagination_frame.grid_columnconfigure(5, weight=1)
        
        self.page_info = ctk.CTkLabel(self.pagination_frame, text='第 1/1 页', font=('微软雅黑', 12))
        self.page_info.grid(row=0, column=2, padx=10)
        
        self.prev_btn = ctk.CTkButton(self.pagination_frame, text='上一页', command=self.on_prev_page,
                                      width=80, font=('微软雅黑', 12), state='disabled')
        self.prev_btn.grid(row=0, column=1, padx=5)
        
        self.next_btn = ctk.CTkButton(self.pagination_frame, text='下一页', command=self.on_next_page,
                                      width=80, font=('微软雅黑', 12), state='disabled')
        self.next_btn.grid(row=0, column=3, padx=5)
        
        self.delete_btn = ctk.CTkButton(self.pagination_frame, text='删除选中', command=self.on_delete,
                                        width=80, font=('微软雅黑', 12), state='disabled')
        self.delete_btn.grid(row=0, column=4, padx=5)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        self.load_records()
    
    def load_records(self):
        records = self.db_manager.get_completed_records(**self.filter_params)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.total_pages = max(1, (len(records) + self.page_size - 1) // self.page_size)
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_records = records[start:end]
        
        calculator = FeeCalculator(self.db_manager.get_config())
        
        for record in page_records:
            duration = calculator.format_duration(record['duration'] if record['duration'] else 0)
            fee = f"{record['fee']:.2f}" if record['fee'] else '-'
            self.tree.insert('', 'end', values=(record['id'], record['plate_number'],
                                               record['vehicle_type'], record['area'],
                                               record['entry_time'], record['exit_time'] or '-',
                                               duration, fee))
        
        self.page_info.configure(text=f'第 {self.current_page}/{self.total_pages} 页')
        self.prev_btn.configure(state='normal' if self.current_page > 1 else 'disabled')
        self.next_btn.configure(state='normal' if self.current_page < self.total_pages else 'disabled')
    
    def on_search(self):
        plate_number = self.plate_entry.get().strip()
        vehicle_type = self.type_var.get()
        
        self.filter_params = {}
        if plate_number:
            self.filter_params['plate_number'] = plate_number
        if vehicle_type != '全部':
            self.filter_params['vehicle_type'] = vehicle_type
        
        self.current_page = 1
        self.load_records()
    
    def on_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_records()
    
    def on_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_records()
    
    def on_tree_select(self, event):
        selected = self.tree.selection()
        self.delete_btn.configure(state='normal' if selected else 'disabled')
    
    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        record_id = item['values'][0]
        
        confirm = ConfirmDialog(self, '确认删除', '确定要删除这条记录吗？')
        self.wait_window(confirm)
        
        if confirm.result:
            self.db_manager.delete_record(record_id)
            MessageDialog(self, '提示', '记录删除成功')
            self.load_records()
            self.delete_btn.configure(state='disabled')
    
    def on_export(self):
        records = self.db_manager.get_completed_records(**self.filter_params)
        
        if not records:
            MessageDialog(self, '提示', '没有可导出的记录')
            return
        
        export_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'export.csv')
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        
        with open(export_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', '车牌号', '车辆类型', '停放区域', '入场时间', '出场时间', '停放时长(分钟)', '费用(元)'])
            
            for record in records:
                writer.writerow([
                    record['id'],
                    record['plate_number'],
                    record['vehicle_type'],
                    record['area'],
                    record['entry_time'],
                    record['exit_time'] or '',
                    record['duration'] or '',
                    record['fee'] or ''
                ])
        
        MessageDialog(self, '提示', f'记录已导出到:\n{export_path}')
    
    def refresh(self):
        self.load_records()