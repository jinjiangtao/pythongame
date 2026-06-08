
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
        self.packets = []
        self.on_select_callback = on_select_callback
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

        self.tree.bind("&lt;&lt;TreeviewSelect&gt;&gt;", self._on_select)

    def add_packet(self, packet):
        """
        添加数据包到列表
        """
        self.packets.append(packet)
        index = len(self.packets) - 1
        values = (
            index + 1,
            format_timestamp(packet.timestamp),
            packet.src_ip,
            packet.dst_ip,
            packet.protocol,
            packet.length,
            packet.summary
        )
        self.tree.insert("", "end", values=values)

    def clear(self):
        """
        清空列表
        """
        self.packets.clear()
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
            if 0 &lt;= index &lt; len(self.packets):
                self.on_select_callback(self.packets[index])

    def get_packet_count(self):
        """
        获取数据包数量
        """
        return len(self.packets)

    def get_statistics(self):
        """
        获取统计信息
        """
        stats = {
            'total': len(self.packets),
            'TCP': 0,
            'UDP': 0,
            'ICMP': 0,
            'ARP': 0,
            'HTTP': 0,
            'HTTPS': 0,
            'OTHER': 0
        }

        for packet in self.packets:
            proto = packet.protocol
            if proto in stats:
                stats[proto] += 1
            else:
                stats['OTHER'] += 1

        return stats
