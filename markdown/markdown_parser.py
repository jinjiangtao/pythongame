import re

class MarkdownParser:
    def __init__(self):
        self.rules = [
            (r'^#{6}\s+(.+)', r'<h6>\1</h6>'),
            (r'^#{5}\s+(.+)', r'<h5>\1</h5>'),
            (r'^#{4}\s+(.+)', r'<h4>\1</h4>'),
            (r'^#{3}\s+(.+)', r'<h3>\1</h3>'),
            (r'^#{2}\s+(.+)', r'<h2>\1</h2>'),
            (r'^#\s+(.+)', r'<h1>\1</h1>'),
            (r'^\*\*\*(.+)\*\*\*$', r'<strong><em>\1</em></strong>'),
            (r'^\*\*(.+)\*\*$', r'<strong>\1</strong>'),
            (r'^\*(.+)\*$', r'<em>\1</em>'),
            (r'^___$', r'<hr/>'),
            (r'^---$', r'<hr/>'),
            (r'^\*\*\*$', r'<hr/>'),
        ]
    
    def convert(self, markdown):
        lines = markdown.split('\n')
        html_lines = []
        in_code_block = False
        code_language = ""
        
        for line in lines:
            if line.startswith('```'):
                if in_code_block:
                    html_lines.append('</pre></code>')
                    in_code_block = False
                    code_language = ""
                else:
                    in_code_block = True
                    code_language = line[3:].strip()
                    html_lines.append(f'<pre><code>')
                continue
            
            if in_code_block:
                html_lines.append(self.escape_html(line))
                continue
            
            processed_line = self.process_line(line)
            html_lines.append(processed_line)
        
        return '\n'.join(html_lines)
    
    def process_line(self, line):
        original_line = line
        
        for pattern, replacement in self.rules:
            if re.match(pattern, line):
                line = re.sub(pattern, replacement, line)
                break
        
        if line == original_line:
            if line.startswith('> '):
                line = f'<blockquote>{line[2:]}</blockquote>'
            elif line.startswith('- ') or line.startswith('* '):
                line = f'<li>{line[2:]}</li>'
            elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '0.')):
                line = f'<li>{line[2:].lstrip()}</li>'
            elif line.strip() == '':
                line = '<br/>'
            else:
                line = f'<p>{line}</p>'
        
        line = self.process_inline_code(line)
        line = self.process_links(line)
        line = self.process_images(line)
        line = self.process_bold_italic(line)
        
        return line
    
    def process_inline_code(self, line):
        pattern = r'`([^`]+)`'
        return re.sub(pattern, r'<code>\1</code>', line)
    
    def process_links(self, line):
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.sub(pattern, r'<a href="\2">\1</a>', line)
    
    def process_images(self, line):
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        return re.sub(pattern, r'<img src="\2" alt="\1"/>', line)
    
    def process_bold_italic(self, line):
        line = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', line)
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        return line
    
    def escape_html(self, text):
        html_escape_table = {
            '&': '&amp;',
            '"': '&quot;',
            "'": '&#39;',
            '>': '&gt;',
            '<': '&lt;',
        }
        return ''.join(html_escape_table.get(c, c) for c in text)