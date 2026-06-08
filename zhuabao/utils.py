"""
辅助函数文件
提供通用的辅助功能
"""

import datetime
import struct
import socket
import ctypes
import os


def format_timestamp(timestamp):
    """
    将时间戳格式化为可读字符串，精确到微秒
    """
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def mac_to_str(mac_bytes):
    """
    将MAC地址字节转换为字符串
    """
    return ":".join(f"{b:02x}" for b in mac_bytes)


def ip_to_str(ip_bytes):
    """
    将IP地址字节转换为字符串
    """
    return socket.inet_ntoa(ip_bytes)


def format_hex_dump(data):
    """
    格式化十六进制和ASCII显示
    返回一个列表，每个元素是一行的显示文本
    """
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_parts = []
        ascii_chars = []
        for b in chunk:
            hex_parts.append(f"{b:02x}")
            if 32 <= b < 127:
                ascii_chars.append(chr(b))
            else:
                ascii_chars.append(".")
        hex_part = " ".join(hex_parts)
        ascii_part = "".join(ascii_chars)
        offset = f"{i:04x}"
        lines.append(f"{offset}  {hex_part:<48}  {ascii_part}")
    return lines


def check_npcap_installed():
    """
    检查Npcap驱动是否已安装
    增强版检测逻辑：检查多个位置
    """
    # 检查常见的安装路径
    npcap_paths = [
        # 系统路径
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32'),
        # Npcap 默认安装路径
        r"C:\Windows\System32\Npcap",
        r"C:\Program Files\Npcap",
        r"C:\Program Files (x86)\Npcap"
    ]
    
    npcap_files = ['Packet.dll', 'wpcap.dll', 'npf.sys']
    
    print("正在检查 Npcap 安装状态...")
    
    # 检查文件检查
    for check_path in npcap_paths:
        for dll_file in npcap_files:
            try:
                full_path = os.path.join(check_path, dll_file)
                if os.path.exists(full_path):
                    print(f"找到 Npcap 文件: {full_path}")
                    return True
            except:
                continue
    
    # 检查注册表（可选，但可能需要管理员权限才能看到）
    try:
        import winreg
        key_path = r"SOFTWARE\Npcap"
        # 尝试打开注册表查找
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path):
                print("在注册表中找到 Npcap 安装信息")
                return True
        except WindowsError:
            pass
            
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path):
                print("在当前用户注册表中找到 Npcap 信息")
                return True
        except WindowsError:
            pass
    except ImportError:
        pass
    
    print("未找到 Npcap")
    return False


def is_admin():
    """
    检查是否以管理员权限运行
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False
