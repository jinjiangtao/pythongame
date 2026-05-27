import customtkinter as ctk
import tkinter as tk
import re

class MarkdownPreview(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=8)
        
        self.create_widgets()
    
    def create_widgets(self):
        if ctk.get_appearance_mode() == "light":
            bg_color = "#F9F9F9"
            fg_color = "#1A1A1A"
        else:
            bg_color = "#1F1F1F"
            fg_color = "#FFFFFF"
        
        self.text_widget = tk.Text(
            self,
            wrap="word",
            font=("Arial", 14),
            bg=bg_color,
            fg=fg_color,
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            state="disabled"
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    def set_content(self, html_content):
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        
        self.text_widget.insert("1.0", self.html_to_text(html_content))
        
        self.text_widget.configure(state="disabled")
    
    def html_to_text(self, html):
        text = html
        
        text = text.replace("<h1>", "\n").replace("</h1>", "\n\n")
        text = text.replace("<h2>", "\n").replace("</h2>", "\n\n")
        text = text.replace("<h3>", "\n").replace("</h3>", "\n\n")
        text = text.replace("<h4>", "\n").replace("</h4>", "\n\n")
        text = text.replace("<h5>", "\n").replace("</h5>", "\n\n")
        text = text.replace("<h6>", "\n").replace("</h6>", "\n\n")
        text = text.replace("<p>", "\n").replace("</p>", "\n\n")
        text = text.replace("<strong>", "**").replace("</strong>", "**")
        text = text.replace("<b>", "**").replace("</b>", "**")
        text = text.replace("<em>", "*").replace("</em>", "*")
        text = text.replace("<i>", "*").replace("</i>", "*")
        text = text.replace("<code>", "`").replace("</code>", "`")
        text = text.replace("<pre>", "\n```\n").replace("</pre>", "\n```\n")
        text = text.replace("<blockquote>", "\n> ").replace("</blockquote>", "\n")
        text = text.replace("<br>", "\n")
        text = text.replace("<br/>", "\n")
        text = text.replace("<hr>", "\n---\n")
        text = text.replace("</tr>", "\n")
        text = text.replace("</td>", " | ")
        text = text.replace("</th>", " | ")
        text = text.replace("<tr>", "")
        text = text.replace("<td>", "")
        text = text.replace("<th>", "")
        text = text.replace("<table>", "\n")
        text = text.replace("</table>", "\n")
        text = text.replace("&nbsp;", " ")
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        
        text = self.process_lists(text)
        
        text = re.sub(r'<[^>]+>', '', text)
        
        return text.strip()
    
    def process_lists(self, html):
        html = re.sub(r'<ul>\s*<li>([^<]+)</li>\s*</ul>', r'\n- \1', html)
        
        def replace_ol(match):
            content = match.group(1)
            li_items = re.findall(r'<li>([^<]+)</li>', content)
            result = ""
            for i, item in enumerate(li_items, 1):
                result += f"\n{i}. {item}"
            return result
        
        html = re.sub(r'<ol>(.*?)</ol>', replace_ol, html, flags=re.DOTALL)
        
        return html