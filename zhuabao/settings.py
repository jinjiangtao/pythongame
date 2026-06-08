"""
配置常量文件
定义程序中使用的所有常量
"""

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "网络抓包工具"

APP_THEME = "dark"
APPEARANCE_MODE = "dark"

PROGRESS_WIDTH = 300

COLUMNS = ["序号", "时间戳", "源IP", "目的IP", "协议", "长度", "简要信息"]

NPCAP_DOWNLOAD_URL = "https://npcap.com"

REQUIRED_PACKAGES = [
    "customtkinter",
    "pcap-ct"
]

ETHER_TYPE_IP = 0x0800
ETHER_TYPE_ARP = 0x0806

IP_PROTO_ICMP = 1
IP_PROTO_TCP = 6
IP_PROTO_UDP = 17

DEFAULT_FILTER = ""

# 包数量限制选项
MAX_PACKET_OPTIONS = ["1000", "5000", "10000", "20000", "不限"]
DEFAULT_MAX_PACKETS = 10000

# 协议过滤选项
PROTOCOL_OPTIONS = ["全部", "TCP", "UDP", "ICMP", "ARP"]
