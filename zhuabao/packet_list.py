"""
数据包列表组件
显示捕获的数据包列表，支持实时过滤、包数量限制、自动滚屏
"""

import customtkinter as ctk
from tkinter import ttk
from settings import COLUMNS, DEFAULT_MAX_PACKETS
from utils import format_timestamp


class PacketList(ctk.CTkFrame):
    """
    数据包列表组件
    """

    def __init__(self, parent, on_select_callback):
        super().__init__(parent)
        self.packets = []  # 存储所有捕获的数据包
        self.on_select_callback = on_select_callback
        
        # 过滤相关
        self.filter_enabled = False
        self.filter_protocol = "全部"
        self.filter_ports = set()
        
        # 包数量限制
        self.max_packets = DEFAULT_MAX_PACKETS
        
        # 自动滚屏
        self.auto_scroll = True
        self.user_scrolled = False
        
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
        self.tree.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """
        检测用户手动滚动
        """
        self.user_scrolled = True

    def set_filter(self, enabled, protocol="全部", ports_str=""):
        """
        设置过滤条件
        """
        self.filter_enabled = enabled
        self.filter_protocol = protocol
        
        # 解析端口
        self.filter_ports = set()
        if ports_str.strip():
            try:
                port_list = [p.strip() for p in ports_str.split(",")]
                for p in port_list:
                    if p:
                        self.filter_ports.add(int(p))
            except ValueError:
                pass
        
        self._refresh_display()

    def set_max_packets(self, max_packets):
        """
        设置最大包数量
        """
        if max_packets == "不限":
            self.max_packets = None
        else:
            try:
                self.max_packets = int(max_packets)
                # 检查是否需要丢弃旧包
                if self.max_packets is not None and len(self.packets) > self.max_packets:
                    self._trim_old_packets()
            except ValueError:
                pass

    def set_auto_scroll(self, enabled):
        """
        设置自动滚屏
        """
        self.auto_scroll = enabled
        if enabled:
            self.user_scrolled = False

    def add_packet(self, packet):
        """
        添加数据包到列表
        """
        self.packets.append(packet)
        
        # 检查包数量限制
        if self.max_packets is not None and len(self.packets) > self.max_packets:
            self._trim_old_packets()
        
        # 如果未启用过滤或包符合条件，则显示
        if not self.filter_enabled or self._packet_matches_filter(packet):
            self._insert_packet_to_tree(packet, len(self.packets) - 1)

    def _trim_old_packets(self):
        """
        丢弃旧包以保持在最大数量限制内
        """
        if self.max_packets is None:
            return
        
        excess = len(self.packets) - self.max_packets
        if excess > 0:
            self.packets = self.packets[excess:]
            self._refresh_display()

    def _packet_matches_filter(self, packet):
        """
        检查数据包是否符合当前过滤条件
        """
        # 协议过滤
        if self.filter_protocol != "全部":
            proto = packet.protocol
            # 处理 HTTP/HTTPS 作为 TCP 的情况
            if self.filter_protocol == "TCP" and proto in ["TCP", "HTTP", "HTTPS"]:
                pass  # 匹配
            elif proto != self.filter_protocol:
                return False
        
        # 端口过滤
        if self.filter_ports:
            src_port = packet.src_port
            dst_port = packet.dst_port
            try:
                if src_port and int(src_port) in self.filter_ports:
                    return True
                if dst_port and int(dst_port) in self.filter_ports:
                    return True
                return False
            except ValueError:
                return False
        
        return True

    def _refresh_display(self):
        """
        刷新显示的数据包列表
        """
        # 清空当前显示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加符合条件的包
        display_index = 0
        for idx, packet in enumerate(self.packets):
            if not self.filter_enabled or self._packet_matches_filter(packet):
                self._insert_packet_to_tree(packet, idx, display_index)
                display_index += 1

    def _insert_packet_to_tree(self, packet, original_index, display_index=None):
        """
        将数据包插入树状视图
        """
        if display_index is None:
            display_index = original_index
        
        values = (
            display_index + 1,
            format_timestamp(packet.timestamp),
            packet.src_ip,
            packet.dst_ip,
            packet.protocol,
            packet.length,
            packet.summary
        )
        item = self.tree.insert("", "end", values=values, tags=(str(original_index),))
        
        # 自动滚屏
        if self.auto_scroll and not self.user_scrolled:
            self.tree.see(item)

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
            # 获取原始索引（从 tag 中）
            tags = self.tree.item(item, "tags")
            if tags:
                try:
                    original_index = int(tags[0])
                    if 0 <= original_index < len(self.packets):
                        self.on_select_callback(self.packets[original_index])
                except ValueError:
                    pass

    def get_packet_count(self):
        """
        获取总数据包数量
        """
        return len(self.packets)

    def get_displayed_count(self):
        """
        获取当前显示的数据包数量
        """
        return len(self.tree.get_children())

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
