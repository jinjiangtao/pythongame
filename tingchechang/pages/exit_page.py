import customtkinter as ctk
from utils.validators import Validators
from utils.calculator import FeeCalculator
from components.dialogs import MessageDialog, ConfirmDialog

class ExitPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_update_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_update = on_update_callback
        self.current_record = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=3)
        self.search_frame.grid_columnconfigure(2, weight=1)
        
        self.plate_label = ctk.CTkLabel(self.search_frame, text='车牌号:', font=('微软雅黑', 14))
        self.plate_label.grid(row=0, column=0, padx=10, pady=15, sticky='w')
        
        self.plate_entry = ctk.CTkEntry(self.search_frame, width=200, font=('微软雅黑', 14))
        self.plate_entry.grid(row=0, column=1, padx=10, pady=15, sticky='w')
        
        self.search_btn = ctk.CTkButton(self.search_frame, text='查询', command=self.on_search,
                                        width=100, font=('微软雅黑', 14))
        self.search_btn.grid(row=0, column=2, padx=10, pady=15)
        
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='ew')
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=2)
        
        self.type_info_label = ctk.CTkLabel(self.info_frame, text='车辆类型:', font=('微软雅黑', 12))
        self.type_info_label.grid(row=0, column=0, padx=15, pady=10, sticky='w')
        self.type_info = ctk.CTkLabel(self.info_frame, text='-', font=('微软雅黑', 12))
        self.type_info.grid(row=0, column=1, padx=15, pady=10, sticky='w')
        
        self.area_info_label = ctk.CTkLabel(self.info_frame, text='停放区域:', font=('微软雅黑', 12))
        self.area_info_label.grid(row=1, column=0, padx=15, pady=10, sticky='w')
        self.area_info = ctk.CTkLabel(self.info_frame, text='-', font=('微软雅黑', 12))
        self.area_info.grid(row=1, column=1, padx=15, pady=10, sticky='w')
        
        self.entry_info_label = ctk.CTkLabel(self.info_frame, text='入场时间:', font=('微软雅黑', 12))
        self.entry_info_label.grid(row=2, column=0, padx=15, pady=10, sticky='w')
        self.entry_info = ctk.CTkLabel(self.info_frame, text='-', font=('微软雅黑', 12))
        self.entry_info.grid(row=2, column=1, padx=15, pady=10, sticky='w')
        
        self.duration_info_label = ctk.CTkLabel(self.info_frame, text='停放时长:', font=('微软雅黑', 12))
        self.duration_info_label.grid(row=3, column=0, padx=15, pady=10, sticky='w')
        self.duration_info = ctk.CTkLabel(self.info_frame, text='-', font=('微软雅黑', 12))
        self.duration_info.grid(row=3, column=1, padx=15, pady=10, sticky='w')
        
        self.fee_info_label = ctk.CTkLabel(self.info_frame, text='应付费用:', font=('微软雅黑', 14))
        self.fee_info_label.grid(row=4, column=0, padx=15, pady=15, sticky='w')
        self.fee_info = ctk.CTkLabel(self.info_frame, text='-', font=('微软雅黑', 14, 'bold'), text_color='#ff6b6b')
        self.fee_info.grid(row=4, column=1, padx=15, pady=15, sticky='w')
        
        self.exit_btn = ctk.CTkButton(self, text='确认出场', command=self.on_exit,
                                      width=150, font=('微软雅黑', 14), state='disabled')
        self.exit_btn.grid(row=2, column=0, columnspan=2, pady=30)
    
    def on_search(self):
        plate_number = self.plate_entry.get().strip().upper()
        
        valid, msg = Validators.validate_plate_number(plate_number)
        if not valid:
            MessageDialog(self, '提示', msg)
            return
        
        records = self.db_manager.get_active_parking(plate_number)
        
        if not records:
            MessageDialog(self, '提示', '未找到该车辆的入场记录')
            self._clear_info()
            return
        
        self.current_record = records[0]
        config = self.db_manager.get_config()
        calculator = FeeCalculator(config)
        fee, duration = calculator.calculate_fee(self.current_record['vehicle_type'], 
                                                self.current_record['entry_time'])
        
        self.type_info.configure(text=self.current_record['vehicle_type'])
        self.area_info.configure(text=self.current_record['area'])
        self.entry_info.configure(text=self.current_record['entry_time'])
        self.duration_info.configure(text=calculator.format_duration(duration))
        self.fee_info.configure(text=f'{fee:.2f} 元')
        
        self.exit_btn.configure(state='normal')
    
    def _clear_info(self):
        self.current_record = None
        self.type_info.configure(text='-')
        self.area_info.configure(text='-')
        self.entry_info.configure(text='-')
        self.duration_info.configure(text='-')
        self.fee_info.configure(text='-')
        self.exit_btn.configure(state='disabled')
    
    def on_exit(self):
        if not self.current_record:
            return
        
        config = self.db_manager.get_config()
        calculator = FeeCalculator(config)
        fee, duration = calculator.calculate_fee(self.current_record['vehicle_type'], 
                                                self.current_record['entry_time'])
        
        confirm = ConfirmDialog(self, '确认出场', 
                               f'车牌号: {self.current_record["plate_number"]}\n'
                               f'应付费用: {fee:.2f} 元\n\n确定要出场吗？')
        
        self.wait_window(confirm)
        
        if confirm.result:
            self.db_manager.complete_parking(self.current_record['id'], duration, fee)
            MessageDialog(self, '提示', '车辆出场结算成功')
            self._clear_info()
            self.plate_entry.delete(0, 'end')
            self.on_update()
    
    def refresh(self):
        self._clear_info()