import customtkinter as ctk
import tkinter as tk
from tkinter import Menu
from toolbar import Toolbar
from editor import TextEditor
from preview import MarkdownPreview
from statusbar import StatusBar
from file_manager import FileManager
from markdown_parser import MarkdownParser

class MarkdownEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Markdown 编辑器 V2.0")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        self.center_window()
        
        self.current_file = None
        self.is_modified = False
        self.appearance_mode = "light"
        
        self.file_manager = FileManager(self)
        self.markdown_parser = MarkdownParser()
        
        self.create_widgets()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1200x800+{x}+{y}")
    
    def create_widgets(self):
        self.menu_frame = ctk.CTkFrame(self, height=35, fg_color="transparent")
        self.menu_frame.pack(fill="x", padx=10, pady=(5, 0))
        self.menu_frame.pack_propagate(False)
        
        self.menu_items = ["文件", "编辑", "格式", "视图", "帮助"]
        self.menu_buttons = {}
        self.sub_menus = {}
        
        for item in self.menu_items:
            btn = ctk.CTkButton(
                self.menu_frame,
                text=item,
                width=60,
                height=28,
                corner_radius=6,
                fg_color="transparent",
                hover_color="gray20",
                text_color=("gray80", "gray20"),
                font=("Microsoft YaHei", 13),
                command=lambda i=item: self.show_sub_menu(i)
            )
            btn.pack(side="left", padx=2, pady=3)
            self.menu_buttons[item] = btn
            btn.bind("<Enter>", lambda e, i=item: self.on_menu_enter(e, i))
            btn.bind("<Leave>", lambda e, i=item: self.on_menu_leave(e, i))
        
        self.sub_menu_frame = ctk.CTkFrame(self, height=200, corner_radius=8)
        self.sub_menu_frame.pack_propagate(False)
        self.sub_menu_frame.place_forget()
        
        self.create_sub_menu_items()
        
        self.toolbar = Toolbar(self)
        self.toolbar.pack(fill="x", padx=10, pady=(5, 5))
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        
        self.editor_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.editor_frame.pack(side="left", fill="both", expand=True)
        
        self.sizer_frame = ctk.CTkFrame(self.main_frame, width=6, corner_radius=3)
        self.sizer_frame.pack(side="left", fill="y", padx=(2, 2))
        self.sizer_frame.bind("<Button-1>", self.start_resize)
        self.sizer_frame.bind("<B1-Motion>", self.on_resize)
        self.sizer_frame.bind("<ButtonRelease-1>", self.stop_resize)
        self.sizer_frame.configure(cursor="sb_h_double_arrow")
        
        self.preview_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.preview_frame.pack(side="right", fill="both", expand=True)
        
        self.editor = TextEditor(self.editor_frame, self.on_text_change)
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.preview = MarkdownPreview(self.preview_frame)
        self.preview.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.statusbar = StatusBar(self)
        self.statusbar.pack(fill="x", padx=10, pady=(0, 5))
        
        self.toolbar.set_callback("new", self.new_file)
        self.toolbar.set_callback("open", self.open_file)
        self.toolbar.set_callback("save", self.save_file)
        self.toolbar.set_callback("export", self.export_html)
        self.toolbar.set_callback("clear", self.clear_content)
        self.toolbar.set_callback("theme", self.toggle_theme)
        
        self.bind_shortcuts()
    
    def create_sub_menu_items(self):
        self.sub_menu_items = {
            "文件": [
                ("新建", "Ctrl+N", self.new_file),
                ("打开", "Ctrl+O", self.open_file),
                ("保存", "Ctrl+S", self.save_file),
                ("另存为", "Ctrl+Shift+S", self.save_as_file),
                ("-", "", None),
                ("导出HTML", "Ctrl+E", self.export_html),
                ("-", "", None),
                ("退出", "", self.on_closing)
            ],
            "编辑": [
                ("撤销", "Ctrl+Z", self.editor_undo),
                ("重做", "Ctrl+Y", self.editor_redo),
                ("-", "", None),
                ("复制", "Ctrl+C", self.editor_copy),
                ("粘贴", "Ctrl+V", self.editor_paste),
                ("剪切", "Ctrl+X", self.editor_cut),
                ("-", "", None),
                ("全选", "Ctrl+A", self.editor_select_all),
                ("删除", "Delete", self.editor_delete)
            ],
            "格式": [
                ("标题1", "", lambda: self.insert_syntax("# ")),
                ("标题2", "", lambda: self.insert_syntax("## ")),
                ("标题3", "", lambda: self.insert_syntax("### ")),
                ("-", "", None),
                ("加粗", "", lambda: self.insert_syntax("**", "**")),
                ("斜体", "", lambda: self.insert_syntax("*", "*")),
                ("-", "", None),
                ("无序列表", "", lambda: self.insert_syntax("- ")),
                ("有序列表", "", lambda: self.insert_syntax("1. ")),
                ("-", "", None),
                ("代码块", "", lambda: self.insert_syntax("```\n", "\n```")),
                ("引用", "", lambda: self.insert_syntax("> ")),
                ("分割线", "", lambda: self.insert_syntax("\n---\n")),
                ("-", "", None),
                ("链接", "", lambda: self.insert_syntax("[", "](url)")),
                ("图片", "", lambda: self.insert_syntax("![", "](image_url)")),
                ("表格", "", self.insert_table)
            ],
            "视图": [
                ("切换主题", "", self.toggle_theme)
            ],
            "帮助": [
                ("关于", "", self.show_about)
            ]
        }
    
    def on_menu_enter(self, event, menu_name):
        self.show_sub_menu(menu_name)
    
    def on_menu_leave(self, event, menu_name):
        pass
    
    def show_sub_menu(self, menu_name):
        self.sub_menu_frame.place_forget()
        
        for widget in self.sub_menu_frame.winfo_children():
            widget.destroy()
        
        if menu_name not in self.sub_menu_items:
            return
        
        items = self.sub_menu_items[menu_name]
        max_width = 160
        
        for text, shortcut, command in items:
            if text == "-":
                sep = ctk.CTkFrame(self.sub_menu_frame, height=1, width=150, fg_color="gray30")
                sep.pack(fill="x", padx=10, pady=2)
            else:
                btn = ctk.CTkButton(
                    self.sub_menu_frame,
                    text=text,
                    width=max_width,
                    height=28,
                    corner_radius=4,
                    fg_color="transparent",
                    hover_color="gray20",
                    text_color=("gray80", "gray20"),
                    font=("Microsoft YaHei", 12),
                    command=command
                )
                btn.pack(fill="x", padx=2, pady=1)
                
                if shortcut:
                    shortcut_label = ctk.CTkLabel(
                        btn,
                        text=shortcut,
                        font=("Microsoft YaHei", 11),
                        text_color=("gray50", "gray50")
                    )
                    shortcut_label.place(relx=0.8, rely=0.5, anchor="e")
        
        btn_x = self.menu_buttons[menu_name].winfo_rootx()
        btn_y = self.menu_buttons[menu_name].winfo_rooty()
        btn_height = self.menu_buttons[menu_name].winfo_height()
        
        self.sub_menu_frame.configure(width=max_width + 20, height=len(items) * 30 + 10)
        self.sub_menu_frame.place(x=btn_x, y=btn_y + btn_height)
        
        self.sub_menu_frame.lift()
    
    def hide_sub_menu(self, event=None):
        self.sub_menu_frame.place_forget()
    
    def bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-Shift-s>", lambda e: self.save_as_file())
        self.bind("<Control-e>", lambda e: self.export_html())
        
        self.bind("<Button-1>", lambda e: self.hide_sub_menu())
    
    def start_resize(self, event):
        self.resize_start_x = event.x_root
        self.editor_width = self.editor_frame.winfo_width()
        self.main_width = self.main_frame.winfo_width()
    
    def on_resize(self, event):
        delta_x = event.x_root - self.resize_start_x
        new_editor_width = self.editor_width + delta_x
        
        min_width = 200
        max_width = self.main_width - min_width
        
        if new_editor_width < min_width:
            new_editor_width = min_width
        elif new_editor_width > max_width:
            new_editor_width = max_width
        
        ratio = new_editor_width / self.main_width
        
        self.editor_frame.pack_configure(expand=False, fill="y", width=int(self.main_width * ratio))
        self.preview_frame.pack_configure(expand=False, fill="y", width=int(self.main_width * (1 - ratio)))
        
        self.update_idletasks()
    
    def stop_resize(self, event):
        pass
    
    def on_text_change(self):
        content = self.editor.get_content()
        html = self.markdown_parser.convert(content)
        self.preview.set_content(html)
        self.update_status(content)
        self.is_modified = True
    
    def update_status(self, content):
        lines = content.split("\n")
        current_line, current_col = self.editor.get_cursor_position()
        char_count = len(content)
        word_count = len(content.replace(" ", "").replace("\n", ""))
        
        self.statusbar.update_status(
            line=current_line,
            col=current_col,
            char_count=char_count,
            word_count=word_count,
            file_path=self.current_file,
            modified=self.is_modified,
            theme=self.appearance_mode
        )
    
    def insert_syntax(self, prefix, suffix=""):
        self.editor.insert_syntax(prefix, suffix)
    
    def insert_table(self):
        table = "| 列1 | 列2 | 列3 |\n| --- | --- | --- |\n| 内容1 | 内容2 | 内容3 |"
        self.editor.insert_text(table)
    
    def new_file(self):
        self.hide_sub_menu()
        if self.check_save():
            self.editor.clear()
            self.preview.set_content("")
            self.current_file = None
            self.is_modified = False
            self.statusbar.update_status(1, 0, 0, 0, None, False, self.appearance_mode)
            self.title("Markdown 编辑器 V2.0")
    
    def open_file(self):
        self.hide_sub_menu()
        if self.check_save():
            file_path = self.file_manager.open_file()
            if file_path:
                content = self.file_manager.read_file(file_path)
                if content is not None:
                    self.editor.set_content(content)
                    self.current_file = file_path
                    self.is_modified = False
                    self.title(f"Markdown 编辑器 V2.0 - {file_path}")
    
    def save_file(self):
        self.hide_sub_menu()
        if self.current_file:
            content = self.editor.get_content()
            if self.file_manager.write_file(self.current_file, content):
                self.is_modified = False
                self.statusbar.update_modified(False)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        self.hide_sub_menu()
        file_path = self.file_manager.save_file()
        if file_path:
            content = self.editor.get_content()
            if self.file_manager.write_file(file_path, content):
                self.current_file = file_path
                self.is_modified = False
                self.statusbar.update_modified(False)
                self.title(f"Markdown 编辑器 V2.0 - {file_path}")
    
    def export_html(self):
        self.hide_sub_menu()
        content = self.editor.get_content()
        html = self.markdown_parser.convert(content)
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown 导出</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Microsoft YaHei', sans-serif; 
            padding: 60px; 
            max-width: 900px; 
            margin: 0 auto;
            line-height: 1.8;
            color: #333;
            background: #f8f9fa;
        }}
        h1 {{ font-size: 2em; margin-bottom: 0.5em; color: #1a1a1a; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; margin-top: 1.5em; margin-bottom: 0.5em; color: #2a2a2a; }}
        h3 {{ font-size: 1.25em; margin-top: 1.2em; color: #3a3a3a; }}
        h4, h5, h6 {{ font-size: 1em; margin-top: 1em; color: #4a4a4a; }}
        p {{ margin: 1em 0; }}
        code {{ 
            background: #f4f4f4; 
            padding: 2px 8px; 
            border-radius: 4px; 
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }}
        pre {{ 
            background: #2d2d2d; 
            padding: 20px; 
            border-radius: 8px; 
            overflow-x: auto;
            color: #ccc;
        }}
        pre code {{ background: transparent; padding: 0; color: inherit; }}
        blockquote {{ 
            border-left: 4px solid #007bff; 
            margin: 1em 0; 
            padding-left: 16px; 
            color: #666;
            background: #f8f9fa;
            padding: 12px 16px;
            border-radius: 0 6px 6px 0;
        }}
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin: 1em 0;
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 12px; 
            text-align: left; 
        }}
        th {{ 
            background: #f8f8f8; 
            font-weight: 600;
        }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul, ol {{ padding-left: 2em; margin: 1em 0; }}
        li {{ margin: 0.5em 0; }}
        hr {{ 
            border: none; 
            border-top: 1px solid #e0e0e0; 
            margin: 2em 0; 
        }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        self.file_manager.export_html(full_html)
    
    def clear_content(self):
        self.hide_sub_menu()
        if self.check_save():
            self.editor.clear()
            self.preview.set_content("")
            self.is_modified = False
            self.statusbar.update_status(1, 0, 0, 0, self.current_file, False, self.appearance_mode)
    
    def toggle_theme(self):
        self.hide_sub_menu()
        if self.appearance_mode == "light":
            ctk.set_appearance_mode("dark")
            self.appearance_mode = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.appearance_mode = "light"
        
        self.editor.refresh_theme()
        self.preview.refresh_theme()
        self.statusbar.refresh_theme()
    
    def show_about(self):
        self.hide_sub_menu()
        about_window = ctk.CTkToplevel(self)
        about_window.title("关于")
        about_window.geometry("420x220")
        about_window.resizable(False, False)
        about_window.transient(self)
        about_window.grab_set()
        
        frame = ctk.CTkFrame(about_window, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(frame, text="Markdown 编辑器", font=("Microsoft YaHei", 18, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(frame, text="版本 2.0.0", font=("Microsoft YaHei", 14)).pack(pady=5)
        ctk.CTkLabel(frame, text="基于 Python + CustomTkinter 开发", font=("Microsoft YaHei", 12)).pack(pady=5)
        ctk.CTkLabel(frame, text="支持实时预览、语法高亮、主题切换", font=("Microsoft YaHei", 12)).pack(pady=(10, 5))
        
        ctk.CTkButton(frame, text="确定", width=100, height=32, corner_radius=8, command=about_window.destroy).pack(pady=15)
    
    def check_save(self):
        if self.is_modified:
            result = self.message_box("提示", "当前文档已修改，是否保存？")
            if result == "yes":
                self.save_file()
                return True
            elif result == "no":
                return True
            else:
                return False
        return True
    
    def message_box(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(frame, text=message, font=("Microsoft YaHei", 14), wraplength=350).pack(pady=20)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        yes_btn = ctk.CTkButton(btn_frame, text="是", width=80, height=32, corner_radius=6, command=lambda: self.on_msg_btn_click(dialog, "yes"))
        yes_btn.pack(side="left", padx=(0, 10), pady=5)
        
        no_btn = ctk.CTkButton(btn_frame, text="否", width=80, height=32, corner_radius=6, command=lambda: self.on_msg_btn_click(dialog, "no"))
        no_btn.pack(side="left", padx=(0, 10), pady=5)
        
        cancel_btn = ctk.CTkButton(btn_frame, text="取消", width=80, height=32, corner_radius=6, command=lambda: self.on_msg_btn_click(dialog, "cancel"))
        cancel_btn.pack(side="left", pady=5)
        
        self.msg_result = "cancel"
        dialog.wait_window()
        return self.msg_result
    
    def on_msg_btn_click(self, dialog, result):
        self.msg_result = result
        dialog.destroy()
    
    def editor_undo(self):
        self.hide_sub_menu()
        try:
            self.editor.text_widget.edit_undo()
        except:
            pass
    
    def editor_redo(self):
        self.hide_sub_menu()
        try:
            self.editor.text_widget.edit_redo()
        except:
            pass
    
    def editor_copy(self):
        self.editor.text_widget.event_generate("<<Copy>>")
    
    def editor_paste(self):
        self.editor.text_widget.event_generate("<<Paste>>")
    
    def editor_cut(self):
        self.editor.text_widget.event_generate("<<Cut>>")
    
    def editor_select_all(self):
        self.editor.text_widget.tag_add("sel", "1.0", "end")
    
    def editor_delete(self):
        self.editor.text_widget.delete("sel.first", "sel.last")
    
    def on_closing(self):
        if self.check_save():
            self.destroy()