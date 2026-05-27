import customtkinter as ctk
import re

class TextEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change_callback):
        super().__init__(parent, corner_radius=8)
        
        self.on_change_callback = on_change_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        self.text_widget = ctk.CTkTextbox(
            self,
            wrap="word",
            undo=True,
            font=("Consolas", 14),
            corner_radius=8
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.text_widget.bind("<<Modified>>", self.on_modified)
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
    
    def on_modified(self, event):
        if self.text_widget.edit_modified():
            self.text_widget.edit_modified(False)
            self.highlight_syntax()
    
    def on_key_release(self, event):
        if self.on_change_callback:
            self.on_change_callback()
    
    def highlight_syntax(self):
        content = self.text_widget.get("1.0", "end-1c")
        
        tags = ["heading1", "heading2", "heading3", "bold", "italic", "code", "link", "list", "quote"]
        for tag in tags:
            self.text_widget.tag_remove(tag, "1.0", "end")
        
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if line.startswith("### "):
                self.text_widget.tag_add("heading3", f"{i}.0", f"{i}.{len('### ')}")
            elif line.startswith("## "):
                self.text_widget.tag_add("heading2", f"{i}.0", f"{i}.{len('## ')}")
            elif line.startswith("# "):
                self.text_widget.tag_add("heading1", f"{i}.0", f"{i}.{len('# ')}")
            elif line.startswith("- ") or line.startswith("* "):
                self.text_widget.tag_add("list", f"{i}.0", f"{i}.2")
            elif line.startswith("> "):
                self.text_widget.tag_add("quote", f"{i}.0", f"{i}.2")
        
        self.text_widget.tag_config("heading1", font=("Arial", 20, "bold"), foreground="#1a1a1a")
        self.text_widget.tag_config("heading2", font=("Arial", 16, "bold"), foreground="#2a2a2a")
        self.text_widget.tag_config("heading3", font=("Arial", 14, "bold"), foreground="#3a3a3a")
        self.text_widget.tag_config("bold", font=("Arial", 14, "bold"))
        self.text_widget.tag_config("italic", font=("Arial", 14, "italic"))
        self.text_widget.tag_config("code", font=("Consolas", 12), foreground="#0066cc")
        self.text_widget.tag_config("link", foreground="#0066cc", underline=True)
        self.text_widget.tag_config("list", foreground="#0088cc")
        self.text_widget.tag_config("quote", foreground="#666666", font=("Arial", 14, "italic"))
        
        self.highlight_inline_syntax("**", "**", "bold")
        self.highlight_inline_syntax("*", "*", "italic")
        self.highlight_inline_syntax("`", "`", "code")
        self.highlight_link_syntax()
    
    def highlight_inline_syntax(self, start, end, tag):
        content = self.text_widget.get("1.0", "end-1c")
        start_pos = 0
        
        while True:
            start_idx = content.find(start, start_pos)
            if start_idx == -1:
                break
            
            end_idx = content.find(end, start_idx + len(start))
            if end_idx == -1:
                start_pos = start_idx + len(start)
                continue
            
            start_line = content.count("\n", 0, start_idx) + 1
            start_col = start_idx - content.rfind("\n", 0, start_idx)
            
            end_line = content.count("\n", 0, end_idx) + 1
            end_col = end_idx - content.rfind("\n", 0, end_idx) + len(end)
            
            self.text_widget.tag_add(tag, f"{start_line}.{start_col}", f"{end_line}.{end_col}")
            start_pos = end_idx + len(end)
    
    def highlight_link_syntax(self):
        content = self.text_widget.get("1.0", "end-1c")
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for match in re.finditer(pattern, content):
            start_idx = match.start()
            end_idx = match.end()
            
            start_line = content.count("\n", 0, start_idx) + 1
            start_col = start_idx - content.rfind("\n", 0, start_idx)
            
            end_line = content.count("\n", 0, end_idx) + 1
            end_col = end_idx - content.rfind("\n", 0, end_idx)
            
            self.text_widget.tag_add("link", f"{start_line}.{start_col}", f"{end_line}.{end_col}")
    
    def get_content(self):
        return self.text_widget.get("1.0", "end-1c")
    
    def set_content(self, content):
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", content)
        self.highlight_syntax()
    
    def clear(self):
        self.text_widget.delete("1.0", "end")
    
    def insert_text(self, text):
        self.text_widget.insert("insert", text)
    
    def insert_syntax(self, prefix, suffix=""):
        selected_text = self.text_widget.get("sel.first", "sel.last")
        
        if selected_text:
            self.text_widget.delete("sel.first", "sel.last")
            self.text_widget.insert("sel.first", prefix + selected_text + suffix)
        else:
            self.text_widget.insert("insert", prefix + suffix)
            cursor_pos = self.text_widget.index("insert")
            self.text_widget.mark_set("insert", cursor_pos + f"-{len(suffix)}c")
        
        self.highlight_syntax()
    
    def get_cursor_position(self):
        cursor = self.text_widget.index("insert")
        line, col = cursor.split(".")
        return int(line), int(col)