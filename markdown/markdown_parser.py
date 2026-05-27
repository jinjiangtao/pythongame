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
        in_ul = False
        in_ol = False
        ol_counter = 1
        code_language = ""
        
        for i, line in enumerate(lines):
            if line.startswith('```'):
                # Close any open lists first
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    html_lines.append('</ol>')
                    in_ol = False
                    ol_counter = 1
                
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
            
            # Check if it's a list item
            is_ul_item = line.startswith('- ') or line.startswith('* ')
            is_ol_item = False
            if not is_ul_item:
                is_ol_item = re.match(r'^\d+\.\s', line) is not None
            
            # Close lists if not continuing a list
            if in_ul and not is_ul_item:
                html_lines.append('</ul>')
                in_ul = False
            if in_ol and not is_ol_item:
                html_lines.append('</ol>')
                in_ol = False
                ol_counter = 1
            
            if is_ul_item:
                if not in_ul:
                    html_lines.append('<ul>')
                    in_ul = True
                # Just add the li without wrapping
                processed_line = self.process_line(line[2:], is_list_item=True)
                html_lines.append(f'<li>{processed_line}</li>')
            elif is_ol_item:
                if not in_ol:
                    html_lines.append('<ol>')
                    in_ol = True
                # Extract the number and content
                num_match = re.match(r'^(\d+)\.\s*(.*)', line)
                if num_match:
                    content = num_match.group(2)
                    processed_line = self.process_line(content, is_list_item=True)
                    html_lines.append(f'<li>{processed_line}</li>')
                    ol_counter += 1
                else:
                    html_lines.append(f'<li>{line}</li>')
            else:
                processed_line = self.process_line(line)
                html_lines.append(processed_line)
        
        # Close any remaining open tags
        if in_ul:
            html_lines.append('</ul>')
        if in_ol:
            html_lines.append('</ol>')
        
        return '\n'.join(html_lines)
    
    def process_line(self, line, is_list_item=False):
        original_line = line
        
        for pattern, replacement in self.rules:
            if re.match(pattern, line):
                line = re.sub(pattern, replacement, line)
                break
        
        if line == original_line and not is_list_item:
            if line.startswith('> '):
                line = f'<blockquote>{line[2:]}</blockquote>'
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