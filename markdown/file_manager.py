import os
import tkinter as tk
from tkinter import filedialog

class FileManager:
    def __init__(self, parent):
        self.parent = parent
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="打开 Markdown 文件",
            filetypes=[("Markdown 文件", "*.md"), ("文本文件", "*.txt"), ("所有文件", "*.*")],
            parent=self.parent
        )
        return file_path if file_path else None
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="保存 Markdown 文件",
            defaultextension=".md",
            filetypes=[("Markdown 文件", "*.md"), ("文本文件", "*.txt"), ("所有文件", "*.*")],
            parent=self.parent
        )
        return file_path if file_path else None
    
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            self.show_error(f"文件打开失败: {str(e)}")
            return None
    
    def write_file(self, file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            self.show_error(f"文件保存失败: {str(e)}")
            return False
    
    def export_html(self, html_content):
        file_path = filedialog.asksaveasfilename(
            title="导出为 HTML 文件",
            defaultextension=".html",
            filetypes=[("HTML 文件", "*.html"), ("所有文件", "*.*")],
            parent=self.parent
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                self.show_info("导出成功", "HTML 文件已成功导出")
                return True
            except Exception as e:
                self.show_error(f"导出失败: {str(e)}")
                return False
        return False
    
    def show_error(self, message):
        dialog = tk.Toplevel(self.parent)
        dialog.title("错误")
        dialog.geometry("300x120")
        dialog.transient(self.parent)
        
        label = tk.Label(dialog, text=message, padx=20, pady=20)
        label.pack()
        
        button = tk.Button(dialog, text="确定", command=dialog.destroy)
        button.pack(pady=10)
    
    def show_info(self, title, message):
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("300x120")
        dialog.transient(self.parent)
        
        label = tk.Label(dialog, text=message, padx=20, pady=20)
        label.pack()
        
        button = tk.Button(dialog, text="确定", command=dialog.destroy)
        button.pack(pady=10)