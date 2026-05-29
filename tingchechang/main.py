import customtkinter as ctk
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from data.database import DatabaseManager
from pages.entry_page import EntryPage
from pages.exit_page import ExitPage
from pages.monitor_page import MonitorPage
from pages.query_page import QueryPage
from pages.settings_page import SettingsPage
from pages.system_page import SystemPage

class StatusBar(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent, height=30)
        self.db_manager = db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        
        self.status_label = ctk.CTkLabel(self, text='系统运行正常', font=('微软雅黑', 11))
        self.status_label.grid(row=0, column=0, padx=15, sticky='w')
        
        self.total_spaces_label = ctk.CTkLabel(self, text='总车位: 0', font=('微软雅黑', 11))
        self.total_spaces_label.grid(row=0, column=1, padx=15)
        
        self.occupied_label = ctk.CTkLabel(self, text='已停车: 0', font=('微软雅黑', 11))
        self.occupied_label.grid(row=0, column=2, padx=15)
        
        self.available_label = ctk.CTkLabel(self, text='空闲: 0', font=('微软雅黑', 11))
        self.available_label.grid(row=0, column=3, padx=15)
        
        self.time_label = ctk.CTkLabel(self, text='', font=('微软雅黑', 11))
        self.time_label.grid(row=0, column=4, padx=15)
        
        self.update_time()
        self.update_status()
    
    def update_time(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.configure(text=now)
        self.after(1000, self.update_time)
    
    def update_status(self):
        space_count = self.db_manager.get_space_count()
        self.total_spaces_label.configure(text=f'总车位: {space_count["total"]}')
        self.occupied_label.configure(text=f'已停车: {space_count["occupied"]}')
        self.available_label.configure(text=f'空闲: {space_count["available"]}')

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.db_manager = DatabaseManager()
        
        self.title(f'{APP_NAME} v{APP_VERSION}')
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.resizable(False, False)
        
        self._center_window()
        
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')
        
        self._create_widgets()
        
        self.protocol('WM_DELETE_WINDOW', self.on_close)
    
    def _center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')
    
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.top_frame = ctk.CTkFrame(self, height=60)
        self.top_frame.grid(row=0, column=0, sticky='ew')
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.top_frame, text=APP_NAME, font=('微软雅黑', 18, 'bold'))
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky='w')
        
        self.theme_switch = ctk.CTkSwitch(self.top_frame, text='深色模式', 
                                         command=self.on_theme_switch)
        self.theme_switch.grid(row=0, column=1, padx=20, pady=15)
        
        self.tabview = ctk.CTkTabview(self, height=WINDOW_HEIGHT - 120)
        self.tabview.grid(row=1, column=0, sticky='nsew')
        
        self.tab_names = ['车辆入场', '车辆出场', '车位监控', '记录查询', '费用设置', '系统管理']
        self.pages = {}
        
        self.tabview.add(self.tab_names[0])
        self.pages[self.tab_names[0]] = EntryPage(self.tabview.tab(self.tab_names[0]), 
                                                  self.db_manager, self.on_update)
        self.pages[self.tab_names[0]].pack(fill='both', expand=True)
        
        self.tabview.add(self.tab_names[1])
        self.pages[self.tab_names[1]] = ExitPage(self.tabview.tab(self.tab_names[1]), 
                                                 self.db_manager, self.on_update)
        self.pages[self.tab_names[1]].pack(fill='both', expand=True)
        
        self.tabview.add(self.tab_names[2])
        self.pages[self.tab_names[2]] = MonitorPage(self.tabview.tab(self.tab_names[2]), 
                                                    self.db_manager, self.on_update)
        self.pages[self.tab_names[2]].pack(fill='both', expand=True)
        
        self.tabview.add(self.tab_names[3])
        self.pages[self.tab_names[3]] = QueryPage(self.tabview.tab(self.tab_names[3]), 
                                                  self.db_manager, self.on_update)
        self.pages[self.tab_names[3]].pack(fill='both', expand=True)
        
        self.tabview.add(self.tab_names[4])
        self.pages[self.tab_names[4]] = SettingsPage(self.tabview.tab(self.tab_names[4]), 
                                                     self.db_manager, self.on_update)
        self.pages[self.tab_names[4]].pack(fill='both', expand=True)
        
        self.tabview.add(self.tab_names[5])
        self.pages[self.tab_names[5]] = SystemPage(self.tabview.tab(self.tab_names[5]), 
                                                   self.db_manager, self.on_update)
        self.pages[self.tab_names[5]].pack(fill='both', expand=True)
        
        self.status_bar = StatusBar(self, self.db_manager)
        self.status_bar.grid(row=2, column=0, sticky='ew')
    
    def on_theme_switch(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode('dark')
        else:
            ctk.set_appearance_mode('light')
    
    def on_update(self):
        self.status_bar.update_status()
        
        current_tab = self.tabview.get()
        if current_tab in self.pages:
            self.pages[current_tab].refresh()
        
        self.pages['车位监控'].refresh()
    
    def on_close(self):
        self.db_manager.close()
        self.destroy()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()