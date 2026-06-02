import tkinter as tk
from PIL import Image, ImageDraw

class Tool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x = 0
        self.start_y = 0
        self.drawing = False
    
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True
    
    def on_drag(self, event):
        pass
    
    def on_release(self, event):
        self.drawing = False
    
    def on_click(self, event):
        pass

class BrushTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_x = 0
        self.last_y = 0
    
    def on_press(self, event):
        super().on_press(event)
        scale = self.canvas.scale
        self.last_x = int(event.x / scale)
        self.last_y = int(event.y / scale)
        self.canvas.save_history()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        scale = self.canvas.scale
        x = int(event.x / scale)
        y = int(event.y / scale)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        self.canvas.draw.line([self.last_x, self.last_y, x, y], 
                            fill=color, width=width)
        self.canvas.redraw()
        
        self.last_x = x
        self.last_y = y

class EraserTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_x = 0
        self.last_y = 0
    
    def on_press(self, event):
        super().on_press(event)
        scale = self.canvas.scale
        self.last_x = int(event.x / scale)
        self.last_y = int(event.y / scale)
        self.canvas.save_history()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        scale = self.canvas.scale
        x = int(event.x / scale)
        y = int(event.y / scale)
        
        color = self.canvas.background_color
        width = self.canvas.get_line_width()
        
        self.canvas.draw.line([self.last_x, self.last_y, x, y], 
                            fill=color, width=width)
        self.canvas.redraw()
        
        self.last_x = x
        self.last_y = y

class LineTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.temp_line = None
        self.image_start_x = 0
        self.image_start_y = 0
    
    def on_press(self, event):
        super().on_press(event)
        scale = self.canvas.scale
        self.image_start_x = int(event.x / scale)
        self.image_start_y = int(event.y / scale)
        self.canvas.save_history()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        if self.temp_line:
            self.canvas.delete(self.temp_line)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        self.temp_line = self.canvas.create_line(
            self.start_x, self.start_y, event.x, event.y,
            fill=color, width=width
        )
    
    def on_release(self, event):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
        
        scale = self.canvas.scale
        x = int(event.x / scale)
        y = int(event.y / scale)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        self.canvas.draw.line([self.image_start_x, self.image_start_y, x, y],
                            fill=color, width=width)
        self.canvas.redraw()
        
        super().on_release(event)
        self.temp_line = None

class RectangleTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.temp_rect = None
        self.fill = False
        self.image_start_x = 0
        self.image_start_y = 0
    
    def set_fill(self, fill):
        self.fill = fill
    
    def on_press(self, event):
        super().on_press(event)
        scale = self.canvas.scale
        self.image_start_x = int(event.x / scale)
        self.image_start_y = int(event.y / scale)
        self.canvas.save_history()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        outline = color
        fill_color = color if self.fill else ""
        
        self.temp_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline=outline, fill=fill_color, width=width
        )
    
    def on_release(self, event):
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
        
        scale = self.canvas.scale
        x = int(event.x / scale)
        y = int(event.y / scale)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        x1, y1 = min(self.image_start_x, x), min(self.image_start_y, y)
        x2, y2 = max(self.image_start_x, x), max(self.image_start_y, y)
        
        if self.fill:
            self.canvas.draw.rectangle([x1, y1, x2, y2], fill=color)
            if width > 0:
                self.canvas.draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
        else:
            self.canvas.draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
        
        self.canvas.redraw()
        
        super().on_release(event)
        self.temp_rect = None

class CircleTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.temp_circle = None
        self.fill = False
        self.image_start_x = 0
        self.image_start_y = 0
    
    def set_fill(self, fill):
        self.fill = fill
    
    def on_press(self, event):
        super().on_press(event)
        scale = self.canvas.scale
        self.image_start_x = int(event.x / scale)
        self.image_start_y = int(event.y / scale)
        self.canvas.save_history()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        if self.temp_circle:
            self.canvas.delete(self.temp_circle)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        outline = color
        fill_color = color if self.fill else ""
        
        self.temp_circle = self.canvas.create_oval(
            self.start_x, self.start_y, event.x, event.y,
            outline=outline, fill=fill_color, width=width
        )
    
    def on_release(self, event):
        if self.temp_circle:
            self.canvas.delete(self.temp_circle)
        
        scale = self.canvas.scale
        x = int(event.x / scale)
        y = int(event.y / scale)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        x1, y1 = min(self.image_start_x, x), min(self.image_start_y, y)
        x2, y2 = max(self.image_start_x, x), max(self.image_start_y, y)
        
        if self.fill:
            self.canvas.draw.ellipse([x1, y1, x2, y2], fill=color)
            if width > 0:
                self.canvas.draw.ellipse([x1, y1, x2, y2], outline=color, width=width)
        else:
            self.canvas.draw.ellipse([x1, y1, x2, y2], outline=color, width=width)
        
        self.canvas.redraw()
        
        super().on_release(event)
        self.temp_circle = None

class FillTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
    
    def on_click(self, event):
        self.canvas.save_history()
        
        x = event.x
        y = event.y
        
        scale = self.canvas.scale
        image_x = int(x / scale)
        image_y = int(y / scale)
        
        fill_color = self.canvas.get_color_rgb()
        self.canvas.flood_fill(image_x, image_y, fill_color)