import customtkinter as ctk
from utils.validators import Validators
from components.dialogs import MessageDialog, ConfirmDialog

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_update_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_update = on_update_callback
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        self.rates_frame = ctk.CTkFrame(self)
        self.rates_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        self.rates_frame.grid_columnconfigure(0, weight=1)
        
        self.rates_label = ctk.CTkLabel(self.rates_frame, text='收费标准设置', font=('微软雅黑', 14, 'bold'))
        self.rates_label.grid(row=0, column=0, padx=15, pady=15, sticky='w')
        
        self.car_types = ['小型车', '大型车', '新能源车']
        self.rate_entries = {}
        
        row = 1
        for car_type in self.car_types:
            label = ctk.CTkLabel(self.rates_frame, text=f'{car_type}费率:', font=('微软雅黑', 12))
            label.grid(row=row, column=0, padx=15, pady=10, sticky='w')
            
            entry = ctk.CTkEntry(self.rates_frame, width=100, font=('微软雅黑', 12))
            entry.grid(row=row, column=1, padx=15, pady=10, sticky='w')
            self.rate_entries[car_type] = entry
            row += 1
        
        self.free_label = ctk.CTkLabel(self.rates_frame, text='免费时长(分钟):', font=('微软雅黑', 12))
        self.free_label.grid(row=row, column=0, padx=15, pady=10, sticky='w')
        self.free_entry = ctk.CTkEntry(self.rates_frame, width=100, font=('微软雅黑', 12))
        self.free_entry.grid(row=row, column=1, padx=15, pady=10, sticky='w')
        row += 1
        
        self.cap_label = ctk.CTkLabel(self.rates_frame, text='单日封顶费用(元):', font=('微软雅黑', 12))
        self.cap_label.grid(row=row, column=0, padx=15, pady=10, sticky='w')
        self.cap_entry = ctk.CTkEntry(self.rates_frame, width=100, font=('微软雅黑', 12))
        self.cap_entry.grid(row=row, column=1, padx=15, pady=10, sticky='w')
        
        self.save_btn = ctk.CTkButton(self.rates_frame, text='保存设置', command=self.on_save,
                                     width=150, font=('微软雅黑', 14))
        self.save_btn.grid(row=row+1, column=0, columnspan=2, pady=20)
        
        self.load_config()
    
    def load_config(self):
        config = self.db_manager.get_config()
        
        for car_type in self.car_types:
            self.rate_entries[car_type].delete(0, 'end')
            self.rate_entries[car_type].insert(0, str(config['rates'].get(car_type, 5.0)))
        
        self.free_entry.delete(0, 'end')
        self.free_entry.insert(0, str(config['free_duration']))
        
        self.cap_entry.delete(0, 'end')
        self.cap_entry.insert(0, str(config['daily_cap']))
    
    def on_save(self):
        confirm = ConfirmDialog(self, '确认保存', '确定要保存收费设置吗？')
        self.wait_window(confirm)
        
        if not confirm.result:
            return
        
        rates = {}
        for car_type in self.car_types:
            value = self.rate_entries[car_type].get().strip()
            valid, msg = Validators.validate_positive_number(value)
            if not valid:
                MessageDialog(self, '提示', f'{car_type}费率{msg}')
                return
            rates[car_type] = float(value)
        
        free_value = self.free_entry.get().strip()
        valid, msg = Validators.validate_positive_number(free_value)
        if not valid:
            MessageDialog(self, '提示', f'免费时长{msg}')
            return
        
        cap_value = self.cap_entry.get().strip()
        valid, msg = Validators.validate_positive_number(cap_value)
        if not valid:
            MessageDialog(self, '提示', f'封顶费用{msg}')
            return
        
        self.db_manager.update_config('rates', rates)
        self.db_manager.update_config('free_duration', int(free_value))
        self.db_manager.update_config('daily_cap', float(cap_value))
        
        MessageDialog(self, '提示', '收费设置保存成功')
        self.on_update()
    
    def refresh(self):
        self.load_config()