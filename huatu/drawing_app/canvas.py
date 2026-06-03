import tkinter as tk
import customtkinter as ctk
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
        self.zoom_callback = None
        
        self.bind_events()
        
        self.redraw()
    
    def set_zoom_callback(self, callback):
        self.zoom_callback = callback
    
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
        
        if self.zoom_callback:
            self.zoom_callback(int(self.scale * 100))
    
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
            
            if self.zoom_callback:
                self.zoom_callback(int(self.scale * 100))
    
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
    
    def show_text_dialog(self, x, y):
        canvas_root_x = self.winfo_rootx()
        canvas_root_y = self.winfo_rooty()
        
        screen_x = x * self.scale + self.offset_x
        screen_y = y * self.scale + self.offset_y
        
        dialog_x = canvas_root_x + screen_x
        dialog_y = canvas_root_y + screen_y
        
        dialog_x = max(0, min(dialog_x, self.winfo_screenwidth() - 420))
        dialog_y = max(0, min(dialog_y, self.winfo_screenheight() - 320))
        
        dialog = tk.Toplevel(self)
        dialog.title("输入文字")
        dialog.geometry(f"400x300+{int(dialog_x)}+{int(dialog_y)}")
        dialog.transient(self)
        dialog.grab_set()
        
        text_frame = ctk.CTkFrame(dialog)
        text_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(text_frame, text="请输入文字:").pack(pady=5)
        
        text_input = ctk.CTkTextbox(text_frame, height=80, width=350, activate_scrollbars=True)
        text_input.pack(pady=5)
        
        dialog.after(100, lambda: text_input.focus())
        
        settings_frame = ctk.CTkFrame(text_frame)
        settings_frame.pack(pady=10, fill="x")
        
        font_frame = ctk.CTkFrame(settings_frame)
        font_frame.pack(pady=5, padx=5, fill="x")
        ctk.CTkLabel(font_frame, text="字体:").pack(side="left", padx=5)
        
        available_fonts = [
            "Arial",
            "Times New Roman",
            "Courier New",
            "Verdana",
            "Georgia",
            "Comic Sans MS",
            "Trebuchet MS",
            "Impact"
        ]
        
        font_var = tk.StringVar(value=available_fonts[0])
        font_menu = ctk.CTkOptionMenu(
            font_frame,
            variable=font_var,
            values=available_fonts,
            width=150
        )
        font_menu.pack(side="left", padx=5)
        
        size_frame = ctk.CTkFrame(settings_frame)
        size_frame.pack(pady=5, padx=5, fill="x")
        ctk.CTkLabel(size_frame, text="字号:").pack(side="left", padx=5)
        
        size_var = tk.IntVar(value=24)
        size_slider = ctk.CTkSlider(
            size_frame,
            from_=12,
            to=72,
            variable=size_var,
            width=200
        )
        size_slider.pack(side="left", padx=5)
        
        size_label = ctk.CTkLabel(size_frame, text="24")
        size_label.pack(side="left", padx=5)
        
        def update_size_label(value):
            size_label.configure(text=str(int(float(value))))
        
        size_slider.configure(command=update_size_label)
        
        color_label = ctk.CTkLabel(settings_frame, text=f"颜色: {self.current_color}")
        color_label.pack(pady=5)
        
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10, padx=10, fill="x")
        
        def on_confirm():
            text = text_input.get("1.0", "end-1c").strip()
            if text:
                font_name = font_var.get()
                font_size = int(size_var.get())
                self.draw_text(x, y, text, font_name, font_size, self.current_color)
                self.redraw()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="确认",
            command=on_confirm,
            width=100
        )
        confirm_btn.pack(side="left", padx=10, expand=True)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="取消",
            command=on_cancel,
            width=100
        )
        cancel_btn.pack(side="left", padx=10, expand=True)
        
        dialog.bind("<Return>", lambda e: on_confirm())
        dialog.bind("<Escape>", lambda e: on_cancel())
        
        dialog.wait_window()
    
    def draw_text(self, x, y, text, font_name="Arial", font_size=24, color="#000000"):
        from PIL import ImageFont
        import os
        
        def contains_chinese(s):
            for char in s:
                if '\u4e00' <= char <= '\u9fff':
                    return True
            return False
        
        chinese_fonts = [
            "simhei.ttf",
            "simkai.ttf", 
            "simsun.ttc",
            "msyh.ttc",
            "msyhl.ttc",
            "kaiti.ttf",
            "simfang.ttf"
        ]
        
        font_paths = [
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font)
            for font in chinese_fonts
        ]
        
        font = None
        has_chinese = contains_chinese(text)
        
        if has_chinese:
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                        break
                    except:
                        continue
        else:
            try:
                font = ImageFont.truetype(font_name.lower() + ".ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    pass
        
        if font is None:
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, font_size)
                        break
                    except:
                        continue
        
        if font is None:
            font = ImageFont.load_default()
        
        self.draw.text((x, y), text, fill=color, font=font)