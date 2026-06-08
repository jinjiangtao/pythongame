
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
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 &lt;= b &lt; 127 else "." for b in chunk)
        offset = f"{i:04x}"
        lines.append(f"{offset}  {hex_part:&lt;48}  {ascii_part}")
    return lines


def check_npcap_installed():
    """
    检查Npcap驱动是否已安装
    """
    try:
        system32 = os.path.join(os.environ['SystemRoot'], 'System32')
        if os.path.exists(os.path.join(system32, 'Packet.dll')):
            return True
        if os.path.exists(os.path.join(system32, 'wpcap.dll')):
            return True
        return False
    except Exception:
        return False


def is_admin():
    """
    检查是否以管理员权限运行
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False
