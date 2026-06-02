import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from canvas import DrawingCanvas
from tools import BrushTool, EraserTool, LineTool, RectangleTool, CircleTool, FillTool

class DrawingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("简易画图板")
        self.geometry("1000x700")
        self.resizable(False, False)
        
        self.canvas_frame = None
        self.canvas = None
        self.status_bar = None
        
        self.tools = {}
        self.current_tool_name = "brush"
        self.fill_mode = False
        
        self.init_menubar()
        self.init_layout()
        
        self.update_status("就绪")
    
    def init_menubar(self):
        menubar = tk.Menu(self)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.new_canvas, accelerator="Ctrl+N")
        file_menu.add_command(label="打开", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="保存", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="文件", menu=file_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="撤销", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="重做", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="清空画布", command=self.clear_canvas)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.config(menu=menubar)
        
        self.bind_all("<Control-n>", lambda e: self.new_canvas())
        self.bind_all("<Control-o>", lambda e: self.open_image())
        self.bind_all("<Control-s>", lambda e: self.save_image())
        self.bind_all("<Control-z>", lambda e: self.undo())
        self.bind_all("<Control-y>", lambda e: self.redo())
    
    def init_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        self.create_toolbar()
        self.create_canvas()
        self.create_status_bar()
    
    def create_toolbar(self):
        toolbar = ctk.CTkFrame(self, width=150, corner_radius=0)
        toolbar.grid(row=0, column=0, sticky="ns")
        toolbar.grid_propagate(False)
        
        self.create_tool_buttons(toolbar)
        self.create_color_picker(toolbar)
        self.create_line_width_slider(toolbar)
        self.create_fill_checkbox(toolbar)
    
    def create_tool_buttons(self, parent):
        tools_frame = ctk.CTkFrame(parent)
        tools_frame.pack(pady=10, padx=5, fill="x")
        
        tool_buttons = [
            ("brush", "画笔"),
            ("eraser", "橡皮擦"),
            ("line", "直线"),
            ("rectangle", "矩形"),
            ("circle", "圆形"),
            ("fill", "填充"),
        ]
        
        for tool_name, label in tool_buttons:
            btn = ctk.CTkButton(
                tools_frame, 
                text=label,
                command=lambda name=tool_name: self.select_tool(name),
                width=120,
                height=35
            )
            btn.pack(pady=3)
            self.tools[tool_name] = btn
    
    def create_color_picker(self, parent):
        color_frame = ctk.CTkFrame(parent)
        color_frame.pack(pady=10, padx=5, fill="x")
        
        ctk.CTkLabel(color_frame, text="颜色选择").pack(pady=5)
        
        colors_frame = ctk.CTkFrame(color_frame)
        colors_frame.pack(pady=5)
        
        preset_colors = [
            "#000000", "#ffffff", "#ff0000", "#00ff00", "#0000ff",
            "#ffff00", "#ff00ff", "#00ffff", "#ff8800", "#8800ff",
            "#0088ff", "#88ff00", "#888888", "#ff8888", "#88ff88"
        ]
        
        color_row = 0
        color_col = 0
        
        for color in preset_colors:
            btn = ctk.CTkButton(
                colors_frame,
                width=25,
                height=25,
                fg_color=color,
                hover_color=color,
                command=lambda c=color: self.set_color(c)
            )
            btn.grid(row=color_row, column=color_col, padx=2, pady=2)
            color_col += 1
            if color_col >= 5:
                color_col = 0
                color_row += 1
        
        custom_color_btn = ctk.CTkButton(
            color_frame,
            text="自定义",
            width=120,
            height=25,
            command=self.choose_custom_color
        )
        custom_color_btn.pack(pady=5)
    
    def create_line_width_slider(self, parent):
        width_frame = ctk.CTkFrame(parent)
        width_frame.pack(pady=10, padx=5, fill="x")
        
        ctk.CTkLabel(width_frame, text="画笔粗细").pack(pady=5)
        
        self.width_slider = ctk.CTkSlider(
            width_frame,
            from_=1,
            to=20,
            command=self.update_line_width,
            width=120
        )
        self.width_slider.set(2)
        self.width_slider.pack(pady=5)
        
        self.width_label = ctk.CTkLabel(width_frame, text="2 像素")
        self.width_label.pack()
    
    def create_fill_checkbox(self, parent):
        fill_frame = ctk.CTkFrame(parent)
        fill_frame.pack(pady=10, padx=5, fill="x")
        
        self.fill_var = ctk.BooleanVar()
        fill_checkbox = ctk.CTkCheckBox(
            fill_frame,
            text="填充形状",
            variable=self.fill_var,
            command=self.update_fill_mode
        )
        fill_checkbox.pack(pady=5)
    
    def create_canvas(self):
        self.canvas_frame = ctk.CTkFrame(self, corner_radius=0)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        
        canvas_container = ctk.CTkScrollableFrame(self.canvas_frame, width=850, height=650)
        canvas_container.grid(row=0, column=0, sticky="nsew")
        canvas_container.grid_columnconfigure(0, weight=1)
        canvas_container.grid_rowconfigure(0, weight=1)
        
        self.canvas = DrawingCanvas(canvas_container, width=850, height=650)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.init_tools()
    
    def init_tools(self):
        self.brush_tool = BrushTool(self.canvas)
        self.eraser_tool = EraserTool(self.canvas)
        self.line_tool = LineTool(self.canvas)
        self.rectangle_tool = RectangleTool(self.canvas)
        self.circle_tool = CircleTool(self.canvas)
        self.fill_tool = FillTool(self.canvas)
        
        self.select_tool("brush")
    
    def create_status_bar(self):
        self.status_bar = ctk.CTkLabel(
            self,
            text="就绪",
            height=25,
            fg_color="gray80"
        )
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
    
    def select_tool(self, tool_name):
        self.current_tool_name = tool_name
        
        for name, btn in self.tools.items():
            if name == tool_name:
                btn.configure(fg_color="#1a73e8")
            else:
                btn.configure(fg_color="gray70")
        
        if tool_name == "brush":
            self.canvas.set_tool(self.brush_tool)
        elif tool_name == "eraser":
            self.canvas.set_tool(self.eraser_tool)
        elif tool_name == "line":
            self.canvas.set_tool(self.line_tool)
        elif tool_name == "rectangle":
            self.canvas.set_tool(self.rectangle_tool)
        elif tool_name == "circle":
            self.canvas.set_tool(self.circle_tool)
        elif tool_name == "fill":
            self.canvas.set_tool(self.fill_tool)
    
    def set_color(self, color):
        self.canvas.set_color(color)
    
    def choose_custom_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.set_color(color)
    
    def update_line_width(self, value):
        width = int(value)
        self.canvas.set_line_width(width)
        self.width_label.configure(text=f"{width} 像素")
    
    def update_fill_mode(self):
        self.fill_mode = self.fill_var.get()
        self.rectangle_tool.set_fill(self.fill_mode)
        self.circle_tool.set_fill(self.fill_mode)
    
    def update_status(self, text):
        if self.status_bar:
            self.status_bar.configure(text=text)
    
    def new_canvas(self):
        if self.canvas.can_undo():
            result = messagebox.askyesnocancel(
                "提示",
                "当前画布有未保存的内容，是否保存？"
            )
            if result is True:
                self.save_image()
            elif result is None:
                return
        
        self.canvas.new_canvas()
        self.update_status("新建画布")
    
    def open_image(self):
        if self.canvas.can_undo():
            result = messagebox.askyesnocancel(
                "提示",
                "当前画布有未保存的内容，是否保存？"
            )
            if result is True:
                self.save_image()
            elif result is None:
                return
        
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("PNG 图片", "*.png"),
                ("JPG 图片", "*.jpg"),
                ("BMP 图片", "*.bmp"),
                ("所有图片", "*.*")
            ]
        )
        
        if filepath:
            if self.canvas.open_image(filepath):
                self.update_status(f"已打开: {filepath}")
            else:
                messagebox.showerror("错误", "无法打开图片文件")
    
    def save_image(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG 图片", "*.png"),
                ("JPG 图片", "*.jpg"),
                ("所有文件", "*.*")
            ]
        )
        
        if filepath:
            self.canvas.save_image(filepath)
            self.update_status(f"已保存: {filepath}")
    
    def undo(self):
        if self.canvas.undo():
            self.update_status("撤销")
        else:
            self.update_status("无法撤销")
    
    def redo(self):
        if self.canvas.redo():
            self.update_status("重做")
        else:
            self.update_status("无法重做")
    
    def clear_canvas(self):
        result = messagebox.askyesno("确认", "确定要清空画布吗？")
        if result:
            self.canvas.clear()
            self.update_status("画布已清空")
    
    def show_about(self):
        messagebox.showinfo(
            "关于",
            "简易画图板 v1.0\n\n一个功能实用的绘图工具，支持多种绘图工具和撤销功能。"
        )