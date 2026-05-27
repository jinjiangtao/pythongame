import customtkinter as ctk
import tkinter as tk
import re

class MarkdownPreview(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=8)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.text_widget = tk.Text(
            self,
            wrap="word",
            font=("Microsoft YaHei", 14),
            bg=self.get_bg_color(),
            fg=self.get_fg_color(),
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=12,
            state="disabled",
            spacing1=5,
            spacing2=3,
            spacing3=8
        )
        self.text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.setup_tags()
    
    def get_bg_color(self):
        return "#252525" if ctk.get_appearance_mode() == "dark" else "#ffffff"
    
    def get_fg_color(self):
        return "#e8e8e8" if ctk.get_appearance_mode() == "dark" else "#333333"
    
    def setup_tags(self):
        self.text_widget.tag_config("h1", font=("Microsoft YaHei", 26, "bold"), foreground="#ff6b6b", spacing3=12)
        self.text_widget.tag_config("h2", font=("Microsoft YaHei", 22, "bold"), foreground="#feca57", spacing3=10)
        self.text_widget.tag_config("h3", font=("Microsoft YaHei", 18, "bold"), foreground="#48dbfb", spacing3=8)
        self.text_widget.tag_config("h4", font=("Microsoft YaHei", 16, "bold"), foreground="#1dd1a1", spacing3=6)
        self.text_widget.tag_config("h5", font=("Microsoft YaHei", 14, "bold"), foreground="#5f27cd")
        self.text_widget.tag_config("h6", font=("Microsoft YaHei", 13, "bold"), foreground="#ff9ff3")
        self.text_widget.tag_config("bold", font=("Microsoft YaHei", 14, "bold"))
        self.text_widget.tag_config("italic", font=("Microsoft YaHei", 14, "italic"))
        self.text_widget.tag_config("code", font=("Consolas", 13), foreground="#ff6b6b", background="#3d3d3d" if ctk.get_appearance_mode() == "dark" else "#f4f4f4", borderwidth=1, relief="flat")
        self.text_widget.tag_config("link", foreground="#48dbfb", underline=True)
        self.text_widget.tag_config("quote", foreground="#a0a0a0", font=("Microsoft YaHei", 14, "italic"), lmargin1=20, lmargin2=20)
        self.text_widget.tag_config("list", lmargin1=20, lmargin2=20)
        self.text_widget.tag_config("codeblock", font=("Consolas", 13), foreground="#e8e8e8" if ctk.get_appearance_mode() == "dark" else "#333333", background="#1e1e1e" if ctk.get_appearance_mode() == "dark" else "#f4f4f4", spacing1=6, spacing3=6, lmargin1=15)
    
    def set_content(self, html_content):
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        
        parsed_content = self.parse_html(html_content)
        self.insert_parsed_content(parsed_content)
        
        self.text_widget.configure(state="disabled")
    
    def parse_html(self, html):
        elements = []
        lines = html.split('\n')
        
        in_code_block = False
        code_content = []
        in_ul = False
        in_ol = False
        ol_counter = 1
        
        for line in lines:
            if line.startswith('<pre><code>'):
                in_code_block = True
                code_content = []
                continue
            
            if line.startswith('</code></pre>'):
                in_code_block = False
                elements.append(('codeblock', '\n'.join(code_content)))
                continue
            
            if in_code_block:
                code_content.append(self.escape_text(line))
                continue
            
            line = line.strip()
            
            if line == '<ul>':
                in_ul = True
                continue
            elif line == '</ul>':
                in_ul = False
                continue
            elif line == '<ol>':
                in_ol = True
                ol_counter = 1
                continue
            elif line == '</ol>':
                in_ol = False
                continue
            elif line.startswith('<li>') and line.endswith('</li>'):
                content = self.parse_inline_elements(line[4:-5])
                if in_ul:
                    elements.append(('list', '- ' + content))
                elif in_ol:
                    elements.append(('list', f'{ol_counter}. ' + content))
                    ol_counter += 1
                continue
            elif line.startswith('<h1>') and line.endswith('</h1>'):
                elements.append(('h1', line[4:-5]))
            elif line.startswith('<h2>') and line.endswith('</h2>'):
                elements.append(('h2', line[4:-5]))
            elif line.startswith('<h3>') and line.endswith('</h3>'):
                elements.append(('h3', line[4:-5]))
            elif line.startswith('<h4>') and line.endswith('</h4>'):
                elements.append(('h4', line[4:-5]))
            elif line.startswith('<h5>') and line.endswith('</h5>'):
                elements.append(('h5', line[4:-5]))
            elif line.startswith('<h6>') and line.endswith('</h6>'):
                elements.append(('h6', line[4:-6]))
            elif line.startswith('<blockquote>') and line.endswith('</blockquote>'):
                elements.append(('quote', line[12:-13]))
            elif line.startswith('<p>') and line.endswith('</p>'):
                elements.append(('p', self.parse_inline_elements(line[3:-4])))
            elif line == '<br/>':
                elements.append(('br', ''))
            elif line == '<hr/>':
                elements.append(('hr', '────────────────────────────────────────'))
        
        return elements
    
    def parse_inline_elements(self, text):
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        
        text = re.sub(r'<strong>([^<]+)</strong>', r'**\1**', text)
        text = re.sub(r'<b>([^<]+)</b>', r'**\1**', text)
        text = re.sub(r'<em>([^<]+)</em>', r'*\1*', text)
        text = re.sub(r'<i>([^<]+)</i>', r'*\1*', text)
        text = re.sub(r'<code>([^<]+)</code>', r'`\1`', text)
        text = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'[\2](\1)', text)
        text = re.sub(r'<img src="([^"]+)" alt="([^"]*)"/>', r'![\2](\1)', text)
        
        return text
    
    def insert_parsed_content(self, elements):
        for i, (element_type, content) in enumerate(elements):
            if element_type == 'br':
                self.text_widget.insert("end", "\n")
            elif element_type == 'hr':
                self.text_widget.insert("end", content + "\n\n")
            elif element_type == 'codeblock':
                self.text_widget.insert("end", content + "\n\n", "codeblock")
            else:
                self.text_widget.insert("end", content + "\n\n", element_type)
    
    def escape_text(self, text):
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        return text
    
    def refresh_theme(self):
        bg_color = self.get_bg_color()
        fg_color = self.get_fg_color()
        
        self.text_widget.config(bg=bg_color, fg=fg_color)
        
        self.text_widget.tag_config("code", background="#3d3d3d" if ctk.get_appearance_mode() == "dark" else "#f4f4f4")
        self.text_widget.tag_config("codeblock", background="#1e1e1e" if ctk.get_appearance_mode() == "dark" else "#f4f4f4")