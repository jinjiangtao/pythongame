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
        
        self.title("Markdown 编辑器")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        self.center_window()
        
        self.current_file = None
        self.is_modified = False
        self.appearance_mode = "light"
        
        self.file_manager = FileManager(self)
        self.markdown_parser = MarkdownParser()
        
        self.create_menu()
        self.create_widgets()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1200x800+{x}+{y}")
    
    def create_menu(self):
        self.menu_bar = Menu(self)
        self.configure(menu=self.menu_bar)
        
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新建", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="打开", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="保存", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="另存为", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="导出为HTML", command=self.export_html, accelerator="Ctrl+E")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.on_closing)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="撤销", command=self.editor_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="重做", command=self.editor_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="复制", command=self.editor_copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="粘贴", command=self.editor_paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="剪切", command=self.editor_cut, accelerator="Ctrl+X")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="全选", command=self.editor_select_all, accelerator="Ctrl+A")
        self.edit_menu.add_command(label="删除", command=self.editor_delete, accelerator="Delete")
        self.menu_bar.add_cascade(label="编辑", menu=self.edit_menu)
        
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="切换主题", command=self.toggle_theme)
        self.menu_bar.add_cascade(label="视图", menu=self.view_menu)
        
        self.format_menu = Menu(self.menu_bar, tearoff=0)
        self.format_menu.add_command(label="标题1", command=lambda: self.insert_syntax("# "))
        self.format_menu.add_command(label="标题2", command=lambda: self.insert_syntax("## "))
        self.format_menu.add_command(label="标题3", command=lambda: self.insert_syntax("### "))
        self.format_menu.add_separator()
        self.format_menu.add_command(label="加粗", command=lambda: self.insert_syntax("**", "**"))
        self.format_menu.add_command(label="斜体", command=lambda: self.insert_syntax("*", "*"))
        self.format_menu.add_separator()
        self.format_menu.add_command(label="无序列表", command=lambda: self.insert_syntax("- "))
        self.format_menu.add_command(label="有序列表", command=lambda: self.insert_syntax("1. "))
        self.format_menu.add_separator()
        self.format_menu.add_command(label="代码块", command=lambda: self.insert_syntax("```\n", "\n```"))
        self.format_menu.add_command(label="引用", command=lambda: self.insert_syntax("> "))
        self.format_menu.add_command(label="分割线", command=lambda: self.insert_syntax("\n---\n"))
        self.format_menu.add_separator()
        self.format_menu.add_command(label="链接", command=lambda: self.insert_syntax("[", "](url)"))
        self.format_menu.add_command(label="图片", command=lambda: self.insert_syntax("![", "](image_url)"))
        self.format_menu.add_command(label="表格", command=self.insert_table)
        self.menu_bar.add_cascade(label="格式", menu=self.format_menu)
        
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="关于", command=self.show_about)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)
        
        self.bind_shortcuts()
    
    def bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-Shift-s>", lambda e: self.save_as_file())
        self.bind("<Control-e>", lambda e: self.export_html())
    
    def create_widgets(self):
        self.toolbar = Toolbar(self)
        self.toolbar.pack(fill="x", padx=10, pady=5)
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        
        self.editor = TextEditor(self.main_frame, self.on_text_change)
        self.editor.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.preview = MarkdownPreview(self.main_frame)
        self.preview.pack(side="right", fill="both", expand=True)
        
        self.statusbar = StatusBar(self)
        self.statusbar.pack(fill="x", padx=10, pady=(0, 5))
        
        self.toolbar.set_callback("new", self.new_file)
        self.toolbar.set_callback("open", self.open_file)
        self.toolbar.set_callback("save", self.save_file)
        self.toolbar.set_callback("export", self.export_html)
        self.toolbar.set_callback("clear", self.clear_content)
        self.toolbar.set_callback("theme", self.toggle_theme)
    
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
            modified=self.is_modified
        )
    
    def insert_syntax(self, prefix, suffix=""):
        self.editor.insert_syntax(prefix, suffix)
    
    def insert_table(self):
        table = "| 列1 | 列2 | 列3 |\n| --- | --- | --- |\n| 内容1 | 内容2 | 内容3 |"
        self.editor.insert_text(table)
    
    def new_file(self):
        if self.check_save():
            self.editor.clear()
            self.preview.set_content("")
            self.current_file = None
            self.is_modified = False
            self.statusbar.update_status(1, 0, 0, 0, None, False)
            self.title("Markdown 编辑器")
    
    def open_file(self):
        if self.check_save():
            file_path = self.file_manager.open_file()
            if file_path:
                content = self.file_manager.read_file(file_path)
                if content is not None:
                    self.editor.set_content(content)
                    self.current_file = file_path
                    self.is_modified = False
                    self.title(f"Markdown 编辑器 - {file_path}")
    
    def save_file(self):
        if self.current_file:
            content = self.editor.get_content()
            if self.file_manager.write_file(self.current_file, content):
                self.is_modified = False
                self.statusbar.update_modified(False)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = self.file_manager.save_file()
        if file_path:
            content = self.editor.get_content()
            if self.file_manager.write_file(file_path, content):
                self.current_file = file_path
                self.is_modified = False
                self.statusbar.update_modified(False)
                self.title(f"Markdown 编辑器 - {file_path}")
    
    def export_html(self):
        content = self.editor.get_content()
        html = self.markdown_parser.convert(content)
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown 导出</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }}
        h1, h2, h3, h4, h5, h6 {{ color: #1a1a1a; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 16px; color: #666; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f8f8f8; }}
        a {{ color: #007bff; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        self.file_manager.export_html(full_html)
    
    def clear_content(self):
        if self.check_save():
            self.editor.clear()
            self.preview.set_content("")
            self.is_modified = False
            self.statusbar.update_status(1, 0, 0, 0, self.current_file, False)
    
    def toggle_theme(self):
        if self.appearance_mode == "light":
            ctk.set_appearance_mode("dark")
            self.appearance_mode = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.appearance_mode = "light"
    
    def show_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("关于")
        about_window.geometry("400x200")
        about_window.resizable(False, False)
        about_window.transient(self)
        
        frame = ctk.CTkFrame(about_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Markdown 编辑器", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(frame, text="版本 1.0.0").pack(pady=5)
        ctk.CTkLabel(frame, text="基于 Python + CustomTkinter 开发").pack(pady=5)
        
        ctk.CTkButton(frame, text="确定", command=about_window.destroy).pack(pady=10)
    
    def check_save(self):
        if self.is_modified:
            result = self.message_box("提示", "当前文档已修改，是否保存？", "yesnocancel")
            if result == "yes":
                self.save_file()
                return True
            elif result == "no":
                return True
            else:
                return False
        return True
    
    def message_box(self, title, message, type="ok"):
        dialog = ctk.CTkInputDialog(text=message, title=title)
        dialog.geometry("400x150")
        
        if type == "yesnocancel":
            pass
        
        result = dialog.get_input()
        if result is None:
            return "cancel"
        return "yes" if result.lower() == "yes" else "no"
    
    def editor_undo(self):
        try:
            self.editor.text_widget.edit_undo()
        except:
            pass
    
    def editor_redo(self):
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