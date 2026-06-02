import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from history import HistoryManager
from utils import flood_fill

class DrawingCanvas(tk.Canvas):
    def __init__(self, parent, width=850, height=700, image_width=1920, image_height=1080, **kwargs):
        super().__init__(parent, width=width, height=height, bg="white", 
                        scrollregion=(0, 0, image_width, image_height), **kwargs)
        
        self.image_width = image_width
        self.image_height = image_height
        self.background_color = (255, 255, 255)
        
        self.image = Image.new("RGB", (image_width, image_height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)
        
        self.tk_image = None
        self.scale = 1.0
        
        self.current_color = "#000000"
        self.line_width = 2
        
        self.history = HistoryManager(max_history=20)
        self.history.save_state(self.image)
        
        self.current_tool = None
        self.bind_events()
        
        self.redraw()
    
    def bind_events(self):
        self.bind("<Button-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.bind("<Motion>", self.on_mouse_move)
    
    def on_mouse_down(self, event):
        if self.current_tool:
            self.current_tool.on_press(event)
    
    def on_mouse_drag(self, event):
        if self.current_tool:
            self.current_tool.on_drag(event)
    
    def on_mouse_up(self, event):
        if self.current_tool:
            self.current_tool.on_release(event)
    
    def on_mouse_move(self, event):
        if hasattr(self.master, 'update_status'):
            scale = self.scale
            image_x = int(event.x / scale)
            image_y = int(event.y / scale)
            self.master.update_status(f"X: {image_x}, Y: {image_y}")
    
    def set_tool(self, tool):
        self.current_tool = tool
    
    def get_color(self):
        return self.current_color
    
    def get_color_rgb(self):
        hex_color = self.current_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def set_color(self, color):
        self.current_color = color
    
    def get_line_width(self):
        return self.line_width
    
    def set_line_width(self, width):
        self.line_width = width
    
    def redraw(self):
        if self.tk_image:
            self.delete("all")
        
        display_width = min(self.image_width, self.winfo_width())
        display_height = min(self.image_height, self.winfo_height())
        
        if display_width > 0 and display_height > 0:
            scaled_image = self.image.resize((display_width, display_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(scaled_image)
            self.scale = display_width / self.image_width
            self.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
    
    def save_history(self):
        self.history.save_state(self.image)
    
    def undo(self):
        return self.history.undo(self)
    
    def redo(self):
        return self.history.redo(self)
    
    def can_undo(self):
        return self.history.can_undo()
    
    def can_redo(self):
        return self.history.can_redo()
    
    def flood_fill(self, x, y, fill_color):
        flood_fill(self, x, y, fill_color)
    
    def clear(self):
        self.image = Image.new("RGB", (self.image_width, self.image_height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.history.clear()
        self.history.save_state(self.image)
        self.redraw()
    
    def save_image(self, filepath):
        if filepath.lower().endswith('.png'):
            self.image.save(filepath, 'PNG')
        elif filepath.lower().endswith('.jpg') or filepath.lower().endswith('.jpeg'):
            self.image.save(filepath, 'JPEG', quality=95)
        else:
            self.image.save(filepath)
    
    def open_image(self, filepath):
        try:
            self.image = Image.open(filepath).convert("RGB")
            self.image_width, self.image_height = self.image.size
            self.draw = ImageDraw.Draw(self.image)
            self.config(scrollregion=(0, 0, self.image_width, self.image_height))
            self.history.clear()
            self.history.save_state(self.image)
            self.redraw()
            return True
        except Exception as e:
            return False
    
    def new_canvas(self, width=1920, height=1080):
        self.image_width = width
        self.image_height = height
        self.image = Image.new("RGB", (width, height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.config(scrollregion=(0, 0, width, height))
        self.history.clear()
        self.history.save_state(self.image)
        self.redraw()