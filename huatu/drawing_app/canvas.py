import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from history import HistoryManager
from utils import flood_fill

class DrawingCanvas(tk.Canvas):
    def __init__(self, parent, width=850, height=650, **kwargs):
        super().__init__(parent, width=width, height=height, bg="white",
                         xscrollincrement=1, yscrollincrement=1, **kwargs)
        
        self.display_width = width
        self.display_height = height
        self.image_width = width
        self.image_height = height
        self.background_color = (255, 255, 255)
        
        self.image = Image.new("RGB", (self.image_width, self.image_height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)
        
        self.tk_image = None
        self.scale = 1.0
        self.min_scale = 0.5
        self.max_scale = 2.0
        
        self.offset_x = 0
        self.offset_y = 0
        
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
        
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<Button-4>", self.on_mouse_wheel)
        self.bind("<Button-5>", self.on_mouse_wheel)
        
        self.bind("<Configure>", self.on_configure)
    
    def on_mouse_down(self, event):
        if self.current_tool:
            canvas_x, canvas_y = self.screen_to_canvas(event.x, event.y)
            event.x = canvas_x
            event.y = canvas_y
            self.current_tool.on_press(event)
    
    def on_mouse_drag(self, event):
        if self.current_tool:
            canvas_x, canvas_y = self.screen_to_canvas(event.x, event.y)
            event.x = canvas_x
            event.y = canvas_y
            self.current_tool.on_drag(event)
    
    def on_mouse_up(self, event):
        if self.current_tool:
            canvas_x, canvas_y = self.screen_to_canvas(event.x, event.y)
            event.x = canvas_x
            event.y = canvas_y
            self.current_tool.on_release(event)
    
    def on_mouse_move(self, event):
        canvas_x, canvas_y = self.screen_to_canvas(event.x, event.y)
        if hasattr(self.master, 'master') and hasattr(self.master.master, 'update_status'):
            self.master.master.update_status(f"X: {int(canvas_x)}, Y: {int(canvas_y)} | 缩放: {int(self.scale * 100)}%")
    
    def on_mouse_wheel(self, event):
        ctrl_pressed = (event.state & 0x4) != 0
        if not ctrl_pressed and event.num in (4, 5):
            ctrl_pressed = True
        
        if ctrl_pressed:
            delta = 0
            if event.num == 4 or event.delta > 0:
                delta = 1
            elif event.num == 5 or event.delta < 0:
                delta = -1
            
            if delta != 0:
                factor = 1.1 if delta > 0 else 0.9
                self.zoom_at(event.x, event.y, factor)
        else:
            if event.delta:
                self.yview_scroll(-1 * (event.delta // 120), "units")
            elif event.num == 4:
                self.yview_scroll(-1, "units")
            elif event.num == 5:
                self.yview_scroll(1, "units")
    
    def on_configure(self, event):
        self.update_scrollregion()
    
    def screen_to_canvas(self, x, y):
        canvas_x = (x - self.offset_x) / self.scale
        canvas_y = (y - self.offset_y) / self.scale
        return canvas_x, canvas_y
    
    def canvas_to_screen(self, x, y):
        screen_x = x * self.scale + self.offset_x
        screen_y = y * self.scale + self.offset_y
        return screen_x, screen_y
    
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
    
    def zoom_at(self, x, y, factor):
        new_scale = self.scale * factor
        if new_scale < self.min_scale or new_scale > self.max_scale:
            return
        
        canvas_x, canvas_y = self.screen_to_canvas(x, y)
        self.scale = new_scale
        self.offset_x = x - canvas_x * self.scale
        self.offset_y = y - canvas_y * self.scale
        
        self.redraw()
        self.update_scrollregion()
    
    def zoom(self, factor, center_viewport=True):
        if center_viewport:
            center_x = self.winfo_width() // 2
            center_y = self.winfo_height() // 2
            self.zoom_at(center_x, center_y, factor)
        else:
            new_scale = self.scale * factor
            if new_scale < self.min_scale or new_scale > self.max_scale:
                return
            self.scale = new_scale
            self.redraw()
            self.update_scrollregion()
    
    def set_zoom(self, scale):
        self.scale = max(self.min_scale, min(self.max_scale, scale))
        self.redraw()
        self.update_scrollregion()
    
    def reset_view(self):
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.xview_moveto(0)
        self.yview_moveto(0)
        self.redraw()
        self.update_scrollregion()
    
    def pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.redraw()
        self.update_scrollregion()
    
    def update_scrollregion(self):
        width = self.image_width * self.scale
        height = self.image_height * self.scale
        self.config(scrollregion=(0, 0, width, height))
    
    def redraw(self):
        self.delete("all")
        
        scaled_width = int(self.image_width * self.scale)
        scaled_height = int(self.image_height * self.scale)
        
        if scaled_width > 0 and scaled_height > 0:
            scaled_image = self.image.resize((scaled_width, scaled_height), Image.Resampling.NEAREST)
            self.tk_image = ImageTk.PhotoImage(scaled_image)
            self.create_image(self.offset_x, self.offset_y, image=self.tk_image, anchor=tk.NW)
    
    def save_history(self):
        self.history.save_state(self.image)
    
    def undo(self):
        result = self.history.undo(self)
        if result:
            self.redraw()
        return result
    
    def redo(self):
        result = self.history.redo(self)
        if result:
            self.redraw()
        return result
    
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
            
            if self.image_width < self.display_width:
                self.image_width = self.display_width
            if self.image_height < self.display_height:
                self.image_height = self.display_height
            
            new_image = Image.new("RGB", (self.image_width, self.image_height), self.background_color)
            new_image.paste(self.image, (0, 0))
            self.image = new_image
            
            self.draw = ImageDraw.Draw(self.image)
            self.history.clear()
            self.history.save_state(self.image)
            self.reset_view()
            return True
        except Exception as e:
            return False
    
    def new_canvas(self, width=None, height=None):
        if width is None:
            width = self.display_width
        if height is None:
            height = self.display_height
        
        self.image_width = width
        self.image_height = height
        self.image = Image.new("RGB", (width, height), self.background_color)
        self.draw = ImageDraw.Draw(self.image)
        self.history.clear()
        self.history.save_state(self.image)
        self.reset_view()
