import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont
import re

class TextEditor(ctk.CTkFrame):
    def __init__(self, parent, on_change_callback):
        super().__init__(parent, corner_radius=8)
        
        self.on_change_callback = on_change_callback
        self.highlight_delay = None
        self.line_numbers = None
        
        self.create_widgets()
    
    def create_widgets(self):
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.line_numbers_frame = ctk.CTkFrame(self.container_frame, width=50, fg_color="transparent")
        self.line_numbers_frame.pack(side="left", fill="y", padx=(0, 5))
        self.line_numbers_frame.pack_propagate(False)
        
        self.line_numbers = tk.Text(
            self.line_numbers_frame,
            width=4,
            padx=8,
            pady=10,
            font=("Consolas", 14),
            bg=self.get_bg_color(),
            fg=self.get_fg_color(),
            borderwidth=0,
            highlightthickness=0,
            state="disabled",
            wrap="none"
        )
        self.line_numbers.pack(fill="both", expand=True)
        
        self.text_widget = tk.Text(
            self.container_frame,
            wrap="word",
            undo=True,
            font=("Consolas", 14),
            bg=self.get_bg_color(),
            fg=self.get_fg_color(),
            insertbackground=self.get_insert_color(),
            selectbackground=self.get_select_color(),
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10
        )
        self.text_widget.pack(fill="both", expand=True)
        
        self.text_widget.bind("<<Modified>>", self.on_modified)
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        self.text_widget.bind("<MouseWheel>", self.sync_line_numbers)
        self.text_widget.bind("<Button-1>", self.on_click)
        
        self.setup_fonts()
        self.setup_tags()
    
    def get_bg_color(self):
        return "#2d2d2d" if ctk.get_appearance_mode() == "dark" else "#f5f5f5"
    
    def get_fg_color(self):
        return "#e8e8e8" if ctk.get_appearance_mode() == "dark" else "#333333"
    
    def get_insert_color(self):
        return "#ffffff" if ctk.get_appearance_mode() == "dark" else "#000000"
    
    def get_select_color(self):
        return "#4a90d9" if ctk.get_appearance_mode() == "dark" else "#b4d5ff"
    
    def setup_fonts(self):
        self.font_heading1 = tkfont.Font(family="Microsoft YaHei", size=22, weight="bold")
        self.font_heading2 = tkfont.Font(family="Microsoft YaHei", size=19, weight="bold")
        self.font_heading3 = tkfont.Font(family="Microsoft YaHei", size=16, weight="bold")
        self.font_heading4 = tkfont.Font(family="Microsoft YaHei", size=14, weight="bold")
        self.font_heading5 = tkfont.Font(family="Microsoft YaHei", size=12, weight="bold")
        self.font_heading6 = tkfont.Font(family="Microsoft YaHei", size=11, weight="bold")
        self.font_bold = tkfont.Font(family="Microsoft YaHei", size=14, weight="bold")
        self.font_italic = tkfont.Font(family="Microsoft YaHei", size=14, slant="italic")
        self.font_code = tkfont.Font(family="Consolas", size=13)
    
    def setup_tags(self):
        self.text_widget.tag_config("heading1", font=self.font_heading1, foreground="#ff6b6b")
        self.text_widget.tag_config("heading2", font=self.font_heading2, foreground="#feca57")
        self.text_widget.tag_config("heading3", font=self.font_heading3, foreground="#48dbfb")
        self.text_widget.tag_config("heading4", font=self.font_heading4, foreground="#1dd1a1")
        self.text_widget.tag_config("heading5", font=self.font_heading5, foreground="#5f27cd")
        self.text_widget.tag_config("heading6", font=self.font_heading6, foreground="#ff9ff3")
        self.text_widget.tag_config("bold", font=self.font_bold, foreground="#ffffff" if ctk.get_appearance_mode() == "dark" else "#000000")
        self.text_widget.tag_config("italic", font=self.font_italic, foreground="#ffffff" if ctk.get_appearance_mode() == "dark" else "#000000")
        self.text_widget.tag_config("code", font=self.font_code, foreground="#ff6b6b", background="#3d3d3d" if ctk.get_appearance_mode() == "dark" else "#f4f4f4")
        self.text_widget.tag_config("link", foreground="#48dbfb", underline=True)
        self.text_widget.tag_config("list", foreground="#1dd1a1")
        self.text_widget.tag_config("quote", foreground="#a0a0a0", font=self.font_italic)
        self.text_widget.tag_config("strikethrough", overstrike=True)
        self.text_widget.tag_config("current_line", background="#3a3a3a" if ctk.get_appearance_mode() == "dark" else "#e8f4fd")
        
        self.text_widget.tag_raise("sel")
    
    def on_modified(self, event):
        if self.text_widget.edit_modified():
            self.text_widget.edit_modified(False)
            if self.highlight_delay:
                self.text_widget.after_cancel(self.highlight_delay)
            self.highlight_delay = self.text_widget.after(80, self.highlight_syntax)
    
    def on_key_release(self, event):
        self.update_line_numbers()
        self.highlight_current_line()
        
        if self.on_change_callback:
            if self.highlight_delay:
                self.text_widget.after_cancel(self.highlight_delay)
            self.highlight_delay = self.text_widget.after(120, self.trigger_change)
    
    def on_click(self, event):
        self.highlight_current_line()
    
    def trigger_change(self):
        if self.on_change_callback:
            self.on_change_callback()
    
    def update_line_numbers(self):
        content = self.text_widget.get("1.0", "end-1c")
        lines = content.split("\n")
        line_count = len(lines)
        
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        
        for i in range(1, line_count + 1):
            self.line_numbers.insert("end", f"{i}\n")
        
        self.line_numbers.config(state="disabled")
        
        self.sync_line_numbers()
    
    def sync_line_numbers(self, event=None):
        self.line_numbers.yview_moveto(self.text_widget.yview()[0])
    
    def highlight_current_line(self):
        self.text_widget.tag_remove("current_line", "1.0", "end")
        
        cursor = self.text_widget.index("insert")
        line_start = cursor.split(".")[0] + ".0"
        line_end = cursor.split(".")[0] + ".end"
        
        self.text_widget.tag_add("current_line", line_start, line_end)
        self.text_widget.tag_lower("current_line")
    
    def highlight_syntax(self):
        content = self.text_widget.get("1.0", "end-1c")
        
        tags = ["heading1", "heading2", "heading3", "heading4", "heading5", "heading6", 
                "bold", "italic", "code", "link", "list", "quote"]
        for tag in tags:
            self.text_widget.tag_remove(tag, "1.0", "end")
        
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            line_len = len(line)
            if line.startswith("###### "):
                self.text_widget.tag_add("heading6", f"{i}.0", f"{i}.{line_len}")
            elif line.startswith("##### "):
                self.text_widget.tag_add("heading5", f"{i}.0", f"{i}.{line_len}")
            elif line.startswith("#### "):
                self.text_widget.tag_add("heading4", f"{i}.0", f"{i}.{line_len}")
            elif line.startswith("### "):
                self.text_widget.tag_add("heading3", f"{i}.0", f"{i}.{line_len}")
            elif line.startswith("## "):
                self.text_widget.tag_add("heading2", f"{i}.0", f"{i}.{line_len}")
            elif line.startswith("# "):
                self.text_widget.tag_add("heading1", f"{i}.0", f"{i}.{line_len}")
            elif line.startswith("- ") or line.startswith("* "):
                self.text_widget.tag_add("list", f"{i}.0", f"{i}.2")
            elif line.startswith("> "):
                self.text_widget.tag_add("quote", f"{i}.0", f"{i}.{line_len}")
        
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
        self.update_line_numbers()
        self.highlight_syntax()
    
    def clear(self):
        self.text_widget.delete("1.0", "end")
        self.update_line_numbers()
    
    def insert_text(self, text):
        self.text_widget.insert("insert", text)
        self.update_line_numbers()
    
    def insert_syntax(self, prefix, suffix=""):
        try:
            selected_text = self.text_widget.get("sel.first", "sel.last")
        except:
            selected_text = ""
        
        if selected_text:
            self.text_widget.delete("sel.first", "sel.last")
            self.text_widget.insert("sel.first", prefix + selected_text + suffix)
        else:
            self.text_widget.insert("insert", prefix + suffix)
            cursor_pos = self.text_widget.index("insert")
            self.text_widget.mark_set("insert", cursor_pos + f"-{len(suffix)}c")
        
        self.update_line_numbers()
        self.highlight_syntax()
    
    def get_cursor_position(self):
        cursor = self.text_widget.index("insert")
        line, col = cursor.split(".")
        return int(line), int(col)
    
    def refresh_theme(self):
        bg_color = self.get_bg_color()
        fg_color = self.get_fg_color()
        
        self.text_widget.config(bg=bg_color, fg=fg_color, insertbackground=self.get_insert_color())
        self.line_numbers.config(bg=bg_color, fg=fg_color)
        
        self.text_widget.tag_config("current_line", background="#3a3a3a" if ctk.get_appearance_mode() == "dark" else "#e8f4fd")
        self.text_widget.tag_config("code", background="#3d3d3d" if ctk.get_appearance_mode() == "dark" else "#f4f4f4")
        self.text_widget.tag_config("bold", foreground="#ffffff" if ctk.get_appearance_mode() == "dark" else "#000000")
        self.text_widget.tag_config("italic", foreground="#ffffff" if ctk.get_appearance_mode() == "dark" else "#000000")
        
        self.highlight_syntax()
        self.update_line_numbers()