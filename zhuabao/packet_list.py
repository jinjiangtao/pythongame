"""
数据包列表组件
显示捕获的数据包列表
"""

import customtkinter as ctk
from tkinter import ttk
from settings import COLUMNS
from utils import format_timestamp


class PacketList(ctk.CTkFrame):
    """
    数据包列表组件
    """

    def __init__(self, parent, on_select_callback):
        super().__init__(parent)
        self.all_packets = []  # 存储所有捕获的数据包
        self.displayed_packets = []  # 存储当前显示的数据包
        self.on_select_callback = on_select_callback
        
        # 过滤条件
        self.filter_enabled = False
        self.filter_ports = set()
        self.filter_protocol = "全部"
        
        self._create_widgets()

    def _create_widgets(self):
        """
        创建界面组件
        """
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = tuple(range(len(COLUMNS)))
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for i, col in enumerate(COLUMNS):
            self.tree.heading(i, text=col)
            self.tree.column(i, width=150, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def add_packet(self, packet):
        """
        添加数据包到列表
        """
        self.all_packets.append(packet)
        self._refresh_display()

    def clear(self):
        """
        清空列表
        """
        self.all_packets.clear()
        self.displayed_packets.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _on_select(self, event):
        """
        列表选择事件
        """
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            index = self.tree.index(item)
            if 0 <= index < len(self.displayed_packets):
                self.on_select_callback(self.displayed_packets[index])

    def get_packet_count(self):
        """
        获取总数据包数量
        """
        return len(self.all_packets)

    def get_displayed_count(self):
        """
        获取当前显示的数据包数量
        """
        return len(self.displayed_packets)

    def get_statistics(self):
        """
        获取统计信息
        """
        stats = {
            'total': len(self.all_packets),
            'TCP': 0,
            'UDP': 0,
            'ICMP': 0,
            'ARP': 0,
            'HTTP': 0,
            'HTTPS': 0,
            'OTHER': 0
        }

        for packet in self.all_packets:
            proto = packet.protocol
            if proto in stats:
                stats[proto] += 1
            else:
                stats['OTHER'] += 1

        return stats

    def set_filter(self, enabled, ports=None, protocol=None):
        """
        设置过滤条件
        """
        self.filter_enabled = enabled
        if ports is not None:
            self.filter_ports = ports
        if protocol is not None:
            self.filter_protocol = protocol
        self._refresh_display()

    def _refresh_display(self):
        """
        刷新显示的数据包
        """
        # 清空当前显示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 筛选数据包
        self.displayed_packets = []
        for packet in self.all_packets:
            if self._matches_filter(packet):
                self.displayed_packets.append(packet)
        
        # 添加到列表
        for i, packet in enumerate(self.displayed_packets):
            values = (
                i + 1,
                format_timestamp(packet.timestamp),
                packet.src_ip,
                packet.dst_ip,
                packet.protocol,
                packet.length,
                packet.summary
            )
            self.tree.insert("", "end", values=values)

    def _matches_filter(self, packet):
        """
        检查数据包是否匹配过滤条件
        """
        if not self.filter_enabled:
            return True
        
        # 协议过滤
        if self.filter_protocol != "全部":
            # 处理特殊情况：HTTP/HTTPS 属于 TCP
            if self.filter_protocol == "TCP":
                if packet.protocol not in ["TCP", "HTTP", "HTTPS"]:
                    return False
            elif packet.protocol != self.filter_protocol:
                return False
        
        # 端口过滤
        if self.filter_ports:
            # 只对 TCP 和 UDP 进行端口过滤
            if packet.protocol in ["TCP", "UDP", "HTTP", "HTTPS"]:
                src_port = int(packet.src_port) if packet.src_port else 0
                dst_port = int(packet.dst_port) if packet.dst_port else 0
                if src_port not in self.filter_ports and dst_port not in self.filter_ports:
                    return False
        
        return True
