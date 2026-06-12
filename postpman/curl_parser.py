import shlex
import re
from typing import Dict, Any, Optional, Tuple
import json


class CurlParser:
    def __init__(self):
        self.method = "GET"
        self.url = ""
        self.headers: Dict[str, str] = {}
        self.body = ""
        self.body_type = "none"
    
    def parse(self, curl_command: str) -> Dict[str, Any]:
        curl_command = curl_command.strip()
        
        if not curl_command:
            raise ValueError("cURL 命令不能为空")
        
        curl_command = self._normalize_command(curl_command)
        
        try:
            tokens = shlex.split(curl_command, posix=False)
        except ValueError as e:
            tokens = self._fallback_split(curl_command)
        
        if not tokens:
            raise ValueError("无法解析 cURL 命令")
        
        if tokens[0].lower() != "curl":
            raise ValueError("无效的 cURL 命令格式，命令必须以 'curl' 开头")
        
        self._parse_tokens(tokens[1:])
        
        self._detect_json_body()
        
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "body": self.body,
            "body_type": self.body_type
        }
    
    def _normalize_command(self, command: str) -> str:
        command = command.strip()
        
        command = re.sub(r'\\\s*\n', ' ', command)
        
        command = re.sub(r'\s+', ' ', command)
        
        return command
    
    def _fallback_split(self, command: str) -> list:
        tokens = []
        current = ""
        in_quotes = False
        quote_char = None
        i = 0
        
        while i < len(command):
            char = command[i]
            
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                i += 1
                continue
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                i += 1
                continue
            
            if char == ' ' and not in_quotes:
                if current:
                    tokens.append(current)
                    current = ""
            else:
                current += char
            
            i += 1
        
        if current:
            tokens.append(current)
        
        return tokens
    
    def _parse_tokens(self, tokens: list):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token in ('-X', '--request'):
                if i + 1 < len(tokens):
                    self.method = tokens[i + 1].upper()
                    i += 2
                    continue
            
            elif token in ('-H', '--header'):
                if i + 1 < len(tokens):
                    self._parse_header(tokens[i + 1])
                    i += 2
                    continue
            
            elif token in ('-d', '--data', '--data-raw', '--data-binary'):
                if i + 1 < len(tokens):
                    self._parse_data(tokens[i + 1])
                    if self.method == "GET":
                        self.method = "POST"
                    i += 2
                    continue
            
            elif token == '--data-urlencode':
                if i + 1 < len(tokens):
                    self._parse_urlencoded_data(tokens[i + 1])
                    if self.method == "GET":
                        self.method = "POST"
                    i += 2
                    continue
            
            elif token in ('-A', '--user-agent'):
                if i + 1 < len(tokens):
                    self.headers["User-Agent"] = tokens[i + 1]
                    i += 2
                    continue
            
            elif token in ('-e', '--referer'):
                if i + 1 < len(tokens):
                    self.headers["Referer"] = tokens[i + 1]
                    i += 2
                    continue
            
            elif token in ('-u', '--user'):
                if i + 1 < len(tokens):
                    self.headers["Authorization"] = f"Basic {tokens[i + 1]}"
                    i += 2
                    continue
            
            elif token in ('-b', '--cookie'):
                if i + 1 < len(tokens):
                    self.headers["Cookie"] = tokens[i + 1]
                    i += 2
                    continue
            
            elif token in ('-I', '--head'):
                self.method = "HEAD"
                i += 1
                continue
            
            elif not token.startswith('-'):
                if self._is_url(token):
                    self.url = token
                i += 1
                continue
            
            i += 1
    
    def _parse_header(self, header_str: str):
        if ':' in header_str:
            key, value = header_str.split(':', 1)
            self.headers[key.strip()] = value.strip()
    
    def _parse_data(self, data_str: str):
        self.body = data_str
        self.body_type = "raw"
    
    def _parse_urlencoded_data(self, data_str: str):
        if '=' in data_str:
            key, value = data_str.split('=', 1)
            self.body = {key: value}
            self.body_type = "x-www-form-urlencoded"
    
    def _is_url(self, token: str) -> bool:
        return token.startswith('http://') or token.startswith('https://') or token.startswith('www.')
    
    def _detect_json_body(self):
        if self.body and self.body_type == "raw":
            try:
                json.loads(self.body)
                if "Content-Type" not in self.headers:
                    self.headers["Content-Type"] = "application/json"
            except (json.JSONDecodeError, TypeError):
                pass
    
    def get_display_name(self, headers: Dict[str, str], method: str, url: str) -> str:
        for key, value in headers.items():
            if key.lower() == 'x-name':
                return value
        
        display_url = url[:30] + "..." if len(url) > 30 else url
        return f"{method} {display_url}"


def parse_curl(curl_command: str) -> Dict[str, Any]:
    parser = CurlParser()
    return parser.parse(curl_command)


def get_display_name(headers: Dict[str, str], method: str, url: str) -> str:
    parser = CurlParser()
    return parser.get_display_name(headers, method, url)