import customtkinter as ctk

class MonitorPage(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_update_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_update = on_update_callback
        self.area_frames = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        
        self.refresh()
    
    def refresh(self):
        for frame in self.area_frames.values():
            frame.destroy()
        
        self.area_frames = {}
        spaces = self.db_manager.get_space_status()
        config = self.db_manager.get_config()
        areas = config['areas']
        
        row = 0
        for area in areas:
            area_frame = ctk.CTkFrame(self.main_frame)
            area_frame.grid(row=row, column=0, padx=10, pady=10, sticky='ew')
            area_frame.grid_columnconfigure(0, weight=1)
            
            area_label = ctk.CTkLabel(area_frame, text=f'{area}', font=('微软雅黑', 14, 'bold'))
            area_label.grid(row=0, column=0, padx=15, pady=10, sticky='w')
            
            space_container = ctk.CTkFrame(area_frame)
            space_container.grid(row=1, column=0, padx=15, pady=10, sticky='ew')
            
            area_spaces = [s for s in spaces if s['area'] == area]
            cols = 6
            for i, space in enumerate(area_spaces):
                row_idx = i // cols
                col_idx = i % cols
                
                space_btn = ctk.CTkButton(space_container, text=f'{space["space_number"]}',
                                        width=60, height=40, font=('微软雅黑', 10))
                
                if space['status'] == 'available':
                    space_btn.configure(fg_color='#5cb85c', hover_color='#4cae4c')
                else:
                    space_btn.configure(fg_color='#d9534f', hover_color='#c9302c',
                                      text=f'{space["space_number"]}\n{space["plate_number"][-4:]}')
                
                space_btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)
            
            self.area_frames[area] = area_frame
            row += 1