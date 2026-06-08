
"""
主窗口界面
整合所有组件
"""

import customtkinter as ctk
from tkinter import messagebox
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, APPEARANCE_MODE, PROGRESS_WIDTH
from sniffer import Sniffer
from packet_list import PacketList
from packet_detail import PacketDetail
from filter_manager import FilterManager
from export_manager import ExportManager


class App(ctk.CTk):
    """
    主应用窗口
    """

    def __init__(self):
        super().__init__()
        self.sniffer = Sniffer()
        self.current_filter = ""
        self._setup_window()
        self._create_widgets()
        self._load_devices()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_window(self):
        """
        设置窗口
        """
        ctk.set_appearance_mode(APPEARANCE_MODE)
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _create_widgets(self):
        """
        创建界面组件
        """
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(top_frame, text="网卡:").pack(side="left", padx=5)
        self.device_combo = ctk.CTkComboBox(top_frame, values=[], state="readonly")
        self.device_combo.pack(side="left", padx=5)

        self.start_btn = ctk.CTkButton(top_frame, text="开始抓包", command=self._toggle_capture)
        self.start_btn.pack(side="left", padx=5)

        self.clear_btn = ctk.CTkButton(top_frame, text="清空列表", command=self._clear_list)
        self.clear_btn.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(top_frame, text="保存PCAP", command=self._save_pcap)
        self.save_btn.pack(side="left", padx=5)

        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.filter_manager = FilterManager(filter_frame, self._on_filter_change)
        self.filter_manager.pack(fill="x", expand=True)

        self.packet_list = PacketList(self, self._on_packet_select)
        self.packet_list.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        self.packet_detail = PacketDetail(self)
        self.packet_detail.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.status_frame, text="就绪 - 已捕获: 0 个包")
        self.status_label.pack(side="left", padx=5)

        self.stats_label = ctk.CTkLabel(self.status_frame, text="")
        self.stats_label.pack(side="right", padx=5)

    def _load_devices(self):
        """
        加载网卡列表
        """
        devices = self.sniffer.get_devices()
        self.device_combo.configure(values=devices)
        if devices:
            self.device_combo.set(devices[0])

    def _toggle_capture(self):
        """
        切换抓包状态
        """
        if self.sniffer.is_running:
            self._stop_capture()
        else:
            self._start_capture()

    def _start_capture(self):
        """
        开始抓包
        """
        device = self.device_combo.get()
        if not device:
            messagebox.showwarning("警告", "请选择网卡")
            return

        if self.sniffer.start(device, self._on_packet, self.current_filter):
            self.start_btn.configure(text="停止抓包")
            self._update_status("正在捕获...")

    def _stop_capture(self):
        """
        停止抓包
        """
        self.sniffer.stop()
        self.start_btn.configure(text="开始抓包")
        self._update_status("已停止")

    def _on_packet(self, packet):
        """
        接收数据包回调
        """
        self.after(0, lambda: self._add_packet_to_list(packet))

    def _add_packet_to_list(self, packet):
        """
        添加数据包到列表
        """
        self.packet_list.add_packet(packet)
        self._update_status()
        self._update_stats()

    def _on_packet_select(self, packet):
        """
        数据包选择回调
        """
        self.packet_detail.display_packet(packet)

    def _on_filter_change(self, filter_str):
        """
        过滤器变化回调
        """
        self.current_filter = filter_str
        if self.sniffer.is_running:
            messagebox.showinfo("提示", "过滤器将在下次开始抓包时生效")

    def _clear_list(self):
        """
        清空列表
        """
        self.packet_list.clear()
        self.packet_detail.clear()
        self._update_status()
        self._update_stats()

    def _save_pcap(self):
        """
        保存PCAP文件
        """
        packets = self.packet_list.packets
        if not packets:
            messagebox.showwarning("警告", "没有可保存的数据包")
            return

        ExportManager.save_pcap(packets)

    def _update_status(self, text=None):
        """
        更新状态
        """
        count = self.packet_list.get_packet_count()
        if text:
            self.status_label.configure(text=f"{text} - 已捕获: {count} 个包")
        else:
            self.status_label.configure(text=f"就绪 - 已捕获: {count} 个包")

    def _update_stats(self):
        """
        更新统计
        """
        stats = self.packet_list.get_statistics()
        stats_text = f"TCP: {stats['TCP']}  UDP: {stats['UDP']}  ICMP: {stats['ICMP']}  ARP: {stats['ARP']}"
        self.stats_label.configure(text=stats_text)

    def _on_close(self):
        """
        窗口关闭事件
        """
        self.sniffer.stop()
        self.destroy()
