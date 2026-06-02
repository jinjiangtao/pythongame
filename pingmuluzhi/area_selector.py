import tkinter as tk
import threading


class AreaSelector:
    def __init__(self, on_select_callback=None):
        self.root = None
        self.canvas = None
        self.start_x = 0
        self.start_y = 0
        self.current_x = 0
        self.current_y = 0
        self.is_drawing = False
        self.rect_id = None
        self.selected_area = None
        self.on_select_callback = on_select_callback
        self.thread = None
    
    def create_selector(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.5)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height,
                               bg='gray', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
    
    def on_mouse_down(self, event):
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y
        self.current_x = event.x
        self.current_y = event.y
    
    def on_mouse_drag(self, event):
        if not self.is_drawing:
            return
        
        self.current_x = event.x
        self.current_y = event.y
        
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        
        x1, y1 = min(self.start_x, self.current_x), min(self.start_y, self.current_y)
        x2, y2 = max(self.start_x, self.current_x), max(self.start_y, self.current_y)
        
        self.rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline='red',
            fill='blue',
            stipple='gray50',
            width=2
        )
    
    def on_mouse_up(self, event):
        if not self.is_drawing:
            return
        
        self.is_drawing = False
        
        x1, y1 = min(self.start_x, self.current_x), min(self.start_y, self.current_y)
        x2, y2 = max(self.start_x, self.current_x), max(self.start_y, self.current_y)
        
        width = x2 - x1
        height = y2 - y1
        
        if width > 10 and height > 10:
            self.selected_area = (x1, y1, width, height)
            if self.on_select_callback:
                self.on_select_callback(self.selected_area)
        
        self.close()
    
    def show(self):
        if self.root is None:
            self.create_selector()
        self.root.deiconify()
    
    def close(self):
        if self.root:
            self.root.destroy()
            self.root = None
    
    def start(self):
        self.show()
        self.root.mainloop()
    
    def get_selected_area(self):
        return self.selected_area


def select_area(callback=None):
    selector = AreaSelector(callback)
    selector.start()
    return selector.get_selected_area()