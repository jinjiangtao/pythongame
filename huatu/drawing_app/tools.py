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
    
    def screen_to_canvas(self, x, y):
        return (x - self.canvas.offset_x) / self.canvas.scale, (y - self.canvas.offset_y) / self.canvas.scale
    
    def canvas_to_screen(self, x, y):
        return x * self.canvas.scale + self.canvas.offset_x, y * self.canvas.scale + self.canvas.offset_y

class BrushTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_x = 0
        self.last_y = 0
    
    def on_press(self, event):
        super().on_press(event)
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.save_history()
        self._draw_point(event.x, event.y)
        self.canvas.redraw()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        self._draw_segment(self.last_x, self.last_y, event.x, event.y)
        self.canvas.redraw()
        
        self.last_x = event.x
        self.last_y = event.y
    
    def _draw_segment(self, x1, y1, x2, y2):
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance == 0:
            distance = 1
        
        step = max(1, width // 4)
        
        for i in range(int(distance) + 1):
            t = i / distance if distance > 0 else 0
            x = x1 + dx * t
            y = y1 + dy * t
            self._draw_point(x, y)
    
    def _draw_point(self, x, y):
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        radius = width // 2
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius
        
        self.canvas.draw.ellipse([x1, y1, x2, y2], fill=color)

class EraserTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_x = 0
        self.last_y = 0
    
    def on_press(self, event):
        super().on_press(event)
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.save_history()
        self._draw_point(event.x, event.y)
        self.canvas.redraw()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        self._draw_segment(self.last_x, self.last_y, event.x, event.y)
        self.canvas.redraw()
        
        self.last_x = event.x
        self.last_y = event.y
    
    def _draw_segment(self, x1, y1, x2, y2):
        color = self.canvas.background_color
        width = self.canvas.get_line_width()
        
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance == 0:
            distance = 1
        
        step = max(1, width // 4)
        
        for i in range(int(distance) + 1):
            t = i / distance if distance > 0 else 0
            x = x1 + dx * t
            y = y1 + dy * t
            self._draw_point(x, y)
    
    def _draw_point(self, x, y):
        color = self.canvas.background_color
        width = self.canvas.get_line_width()
        
        radius = width // 2
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius
        
        self.canvas.draw.ellipse([x1, y1, x2, y2], fill=color)

class LineTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.temp_line = None
    
    def on_press(self, event):
        super().on_press(event)
        self.canvas.save_history()
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        if self.temp_line:
            self.canvas.delete(self.temp_line)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        start_x, start_y = self.canvas_to_screen(self.start_x, self.start_y)
        end_x, end_y = self.canvas_to_screen(event.x, event.y)
        
        self.temp_line = self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=width
        )
    
    def on_release(self, event):
        if self.temp_line:
            self.canvas.delete(self.temp_line)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        self.canvas.draw.line([self.start_x, self.start_y, event.x, event.y],
                            fill=color, width=width)
        self.canvas.redraw()
        
        super().on_release(event)
        self.temp_line = None

class RectangleTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.temp_rect = None
        self.fill = False
    
    def set_fill(self, fill):
        self.fill = fill
    
    def on_press(self, event):
        super().on_press(event)
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
        
        x1, y1 = self.canvas_to_screen(self.start_x, self.start_y)
        x2, y2 = self.canvas_to_screen(event.x, event.y)
        
        self.temp_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=outline, fill=fill_color, width=width
        )
    
    def on_release(self, event):
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        
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
    
    def set_fill(self, fill):
        self.fill = fill
    
    def on_press(self, event):
        super().on_press(event)
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
        
        x1, y1 = self.canvas_to_screen(self.start_x, self.start_y)
        x2, y2 = self.canvas_to_screen(event.x, event.y)
        
        self.temp_circle = self.canvas.create_oval(
            x1, y1, x2, y2,
            outline=outline, fill=fill_color, width=width
        )
    
    def on_release(self, event):
        if self.temp_circle:
            self.canvas.delete(self.temp_circle)
        
        color = self.canvas.get_color()
        width = self.canvas.get_line_width()
        
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        
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
        
        fill_color = self.canvas.get_color_rgb()
        self.canvas.flood_fill(event.x, event.y, fill_color)

class PanTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_pan_x = 0
        self.last_pan_y = 0
    
    def on_press(self, event):
        super().on_press(event)
        self.last_pan_x = event.x
        self.last_pan_y = event.y
    
    def on_drag(self, event):
        if not self.drawing:
            return
        
        dx = event.x - self.last_pan_x
        dy = event.y - self.last_pan_y
        
        self.canvas.pan(dx, dy)
        
        self.last_pan_x = event.x
        self.last_pan_y = event.y

class TextTool(Tool):
    def __init__(self, canvas):
        super().__init__(canvas)
    
    def on_press(self, event):
        self.canvas.save_history()
        self.canvas.show_text_dialog(event.x, event.y)
