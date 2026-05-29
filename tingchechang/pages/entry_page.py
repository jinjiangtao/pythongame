import customtkinter as ctk
from utils.validators import Validators
from components.dialogs import MessageDialog

class EntryPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_update_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_update = on_update_callback
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        
        self.plate_label = ctk.CTkLabel(self, text='车牌号:', font=('微软雅黑', 14))
        self.plate_label.grid(row=0, column=0, padx=20, pady=15, sticky='w')
        self.plate_entry = ctk.CTkEntry(self, width=200, font=('微软雅黑', 14))
        self.plate_entry.grid(row=0, column=1, padx=20, pady=15, sticky='w')
        
        self.type_label = ctk.CTkLabel(self, text='车辆类型:', font=('微软雅黑', 14))
        self.type_label.grid(row=1, column=0, padx=20, pady=15, sticky='w')
        self.type_var = ctk.StringVar(value='小型车')
        self.type_combo = ctk.CTkComboBox(self, variable=self.type_var, 
                                          values=['小型车', '大型车', '新能源车'],
                                          width=200, font=('微软雅黑', 14))
        self.type_combo.grid(row=1, column=1, padx=20, pady=15, sticky='w')
        
        self.area_label = ctk.CTkLabel(self, text='停放区域:', font=('微软雅黑', 14))
        self.area_label.grid(row=2, column=0, padx=20, pady=15, sticky='w')
        self.area_var = ctk.StringVar(value='A区')
        config = self.db_manager.get_config()
        self.area_combo = ctk.CTkComboBox(self, variable=self.area_var, 
                                          values=config['areas'],
                                          width=200, font=('微软雅黑', 14))
        self.area_combo.grid(row=2, column=1, padx=20, pady=15, sticky='w')
        
        self.submit_btn = ctk.CTkButton(self, text='确认入场', command=self.on_submit,
                                        width=150, font=('微软雅黑', 14))
        self.submit_btn.grid(row=3, column=0, columnspan=2, pady=30)
    
    def on_submit(self):
        plate_number = self.plate_entry.get().strip().upper()
        vehicle_type = self.type_var.get()
        area = self.area_var.get()
        
        valid, msg = Validators.validate_plate_number(plate_number)
        if not valid:
            MessageDialog(self, '提示', msg)
            return
        
        active_parking = self.db_manager.get_active_parking(plate_number)
        if active_parking:
            MessageDialog(self, '提示', '该车辆已在停车场内，无法重复入场')
            return
        
        space_count = self.db_manager.get_space_count()
        if space_count['available'] == 0:
            MessageDialog(self, '提示', '车位已满，无法入场')
            return
        
        self.db_manager.add_parking_record(plate_number, vehicle_type, area)
        
        MessageDialog(self, '提示', '车辆入场登记成功')
        
        self.plate_entry.delete(0, 'end')
        self.on_update()
    
    def refresh(self):
        config = self.db_manager.get_config()
        self.area_combo.configure(values=config['areas'])