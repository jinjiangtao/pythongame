import customtkinter as ctk

class MessageDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, icon='info'):
        super().__init__(parent)
        self.title(title)
        self.geometry('300x150')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.label = ctk.CTkLabel(self, text=message, wraplength=250)
        self.label.pack(pady=20, padx=20)
        
        self.button = ctk.CTkButton(self, text='确定', command=self.destroy)
        self.button.pack(pady=10)
        
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry('320x160')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = False
        
        self.label = ctk.CTkLabel(self, text=message, wraplength=280)
        self.label.pack(pady=20, padx=20)
        
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=20, fill='x')
        
        self.yes_btn = ctk.CTkButton(self.frame, text='确定', command=self.on_confirm, width=100)
        self.yes_btn.pack(side='right', padx=5)
        
        self.no_btn = ctk.CTkButton(self.frame, text='取消', command=self.on_cancel, width=100)
        self.no_btn.pack(side='right', padx=5)
        
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_confirm(self):
        self.result = True
        self.destroy()
    
    def on_cancel(self):
        self.result = False
        self.destroy()

class InputDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, default_value=''):
        super().__init__(parent)
        self.title(title)
        self.geometry('350x180')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        
        self.label = ctk.CTkLabel(self, text=message)
        self.label.pack(pady=15, padx=20)
        
        self.entry = ctk.CTkEntry(self, width=250)
        self.entry.insert(0, default_value)
        self.entry.pack(pady=10)
        
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=20, fill='x')
        
        self.ok_btn = ctk.CTkButton(self.frame, text='确定', command=self.on_ok, width=100)
        self.ok_btn.pack(side='right', padx=5)
        
        self.cancel_btn = ctk.CTkButton(self.frame, text='取消', command=self.on_cancel, width=100)
        self.cancel_btn.pack(side='right', padx=5)
        
        self.entry.focus()
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_ok(self):
        self.result = self.entry.get().strip()
        self.destroy()
    
    def on_cancel(self):
        self.result = None
        self.destroy()