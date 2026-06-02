import tkinter as tk
import threading
import time


class AnnotationOverlay:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.is_active = False
        self.is_paused = False
        
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
        
        self.tool = 'pen'
        self.color = 'red'
        self.line_width = 3
        
        self.lines = []
        self.current_line = []
        
        self.overlay_thread = None
        self.running = False
    
    def create_overlay(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-transparentcolor', 'white')
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height,
                               bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        self.hide()
    
    def on_mouse_down(self, event):
        if not self.is_active or self.is_paused:
            return
        
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.current_line = []
        
        if self.tool == 'pen':
            self.current_line.append((event.x, event.y))
    
    def on_mouse_drag(self, event):
        if not self.drawing or not self.is_active or self.is_paused:
            return
        
        if self.tool == 'pen':
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.color, width=self.line_width,
                capstyle=tk.ROUND, joinstyle=tk.ROUND
            )
            self.current_line.append((event.x, event.y))
        
        self.last_x = event.x
        self.last_y = event.y
    
    def on_mouse_up(self, event):
        if self.drawing:
            self.drawing = False
            if self.current_line:
                self.lines.append({
                    'tool': self.tool,
                    'color': self.color,
                    'width': self.line_width,
                    'points': self.current_line.copy()
                })
            self.current_line = []
    
    def set_tool(self, tool):
        self.tool = tool
    
    def set_color(self, color):
        self.color = color
    
    def set_line_width(self, width):
        self.line_width = width
    
    def show(self):
        if self.root:
            self.root.deiconify()
            self.is_active = True
    
    def hide(self):
        if self.root:
            self.root.withdraw()
            self.is_active = False
    
    def clear(self):
        if self.canvas:
            self.canvas.delete('all')
            self.lines = []
    
    def pause(self):
        self.is_paused = True
    
    def resume(self):
        self.is_paused = False
    
    def start(self):
        if self.root is None:
            self.create_overlay()
        
        self.running = True
        self.show()
        
        if self.overlay_thread is None or not self.overlay_thread.is_alive():
            self.overlay_thread = threading.Thread(target=self.run, daemon=True)
            self.overlay_thread.start()
    
    def run(self):
        while self.running:
            try:
                self.root.update()
                time.sleep(0.01)
            except Exception:
                break
    
    def stop(self):
        self.running = False
        self.hide()
        if self.root:
            try:
                self.root.destroy()
                self.root = None
            except Exception:
                pass
        self.overlay_thread = None
    
    def get_lines(self):
        return self.lines.copy()