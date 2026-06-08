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
from export_manager import ExportManager


class App(ctk.CTk):
    """
    主应用窗口
    """

    def __init__(self):
        super().__init__()
        self.sniffer = Sniffer()
        self.max_packets = 5000  # 默认最大包数
        self.auto_scroll = True  # 自动滚屏
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
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def _create_widgets(self):
        """
        创建界面组件
        """
        # 第一行：网卡选择、开始/暂停/停止、清空列表
        top_row1 = ctk.CTkFrame(self)
        top_row1.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        ctk.CTkLabel(top_row1, text="网卡:").pack(side="left", padx=5)
        self.device_combo = ctk.CTkComboBox(top_row1, values=[], state="readonly", width=400)
        self.device_combo.pack(side="left", padx=5)

        self.start_btn = ctk.CTkButton(top_row1, text="开始抓包", command=self._toggle_capture)
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = ctk.CTkButton(top_row1, text="暂停", command=self._toggle_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(top_row1, text="停止", command=self._stop_capture, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        self.clear_btn = ctk.CTkButton(top_row1, text="清空列表", command=self._clear_list)
        self.clear_btn.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(top_row1, text="保存PCAP", command=self._save_pcap)
        self.save_btn.pack(side="left", padx=5)

        # 第二行：协议过滤、端口过滤、启用过滤、清空过滤、自动滚屏、最大包数
        top_row2 = ctk.CTkFrame(self)
        top_row2.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # 协议过滤
        ctk.CTkLabel(top_row2, text="协议:").pack(side="left", padx=5)
        self.protocol_combo = ctk.CTkComboBox(
            top_row2, 
            values=["全部", "TCP", "UDP", "ICMP", "ARP"], 
            state="readonly",
            width=100
        )
        self.protocol_combo.set("全部")
        self.protocol_combo.pack(side="left", padx=5)
        self.protocol_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())

        # 端口过滤
        ctk.CTkLabel(top_row2, text="端口:").pack(side="left", padx=5)
        self.port_entry = ctk.CTkEntry(
            top_row2, 
            placeholder_text="输入端口号，如 80",
            width=150
        )
        self.port_entry.pack(side="left", padx=5)
        self.port_entry.bind("<KeyRelease>", lambda e: self._apply_filter())
        self.port_entry.bind("<Return>", lambda e: self._apply_filter())

        # 启用过滤
        self.enable_filter_var = ctk.BooleanVar(value=False)
        self.enable_filter_check = ctk.CTkCheckBox(
            top_row2, 
            text="启用过滤", 
            variable=self.enable_filter_var,
            command=self._apply_filter
        )
        self.enable_filter_check.pack(side="left", padx=5)

        # 清空过滤
        self.clear_filter_btn = ctk.CTkButton(
            top_row2, 
            text="清空过滤", 
            command=self._clear_filter,
            width=100
        )
        self.clear_filter_btn.pack(side="left", padx=5)

        # 自动滚屏
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        self.auto_scroll_check = ctk.CTkCheckBox(
            top_row2, 
            text="自动滚屏", 
            variable=self.auto_scroll_var
        )
        self.auto_scroll_check.pack(side="left", padx=5)

        # 最大包数
        ctk.CTkLabel(top_row2, text="最大包数:").pack(side="left", padx=5)
        self.max_packets_combo = ctk.CTkComboBox(
            top_row2, 
            values=["1000", "5000", "10000", "50000"], 
            state="readonly",
            width=100
        )
        self.max_packets_combo.set("5000")
        self.max_packets_combo.pack(side="left", padx=5)
        self.max_packets_combo.bind("<<ComboboxSelected>>", lambda e: self._update_max_packets())

        # 数据包列表
        self.packet_list = PacketList(self, self._on_packet_select)
        self.packet_list.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # 数据包详情
        self.packet_detail = PacketDetail(self)
        self.packet_detail.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        # 状态栏
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.status_frame, text="就绪 - 总包数: 0, 显示: 0")
        self.status_label.pack(side="left", padx=5)

        self.stats_label = ctk.CTkLabel(self.status_frame, text="")
        self.stats_label.pack(side="right", padx=5)

    def _load_devices(self):
        """
        加载网卡列表，显示友好名称
        """
        devices = self.sniffer.get_devices()
        self.device_map = {}  # 保存显示名和实际名的映射
        display_names = []
        
        for dev in devices:
            info = self.sniffer.device_info.get(dev, {})
            friendly_name = info.get('friendly_name', dev)
            is_connected = info.get('is_connected', False)
            
            # 构建显示名称
            if is_connected:
                display_name = f"{friendly_name} (已连接)"
            else:
                display_name = f"{friendly_name} (未连接)"
            
            display_names.append(display_name)
            self.device_map[display_name] = dev
        
        self.device_combo.configure(values=display_names)
        
        # 默认选择 Loopback（如果有）
        for i, display_name in enumerate(display_names):
            if "loopback" in display_name.lower() or "127.0.0.1" in display_name:
                self.device_combo.set(display_name)
                print(f"默认选择 Loopback 网卡: {display_name}")
                break
        else:
            if devices:
                self.device_combo.set(display_names[0])
                print(f"默认选择第一个网卡: {display_names[0]}")

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
        display_name = self.device_combo.get()
        if not display_name:
            messagebox.showwarning("警告", "请选择网卡")
            return
            
        device_name = self.device_map.get(display_name, display_name)
        print(f"选择的网卡: {device_name}")

        if self.sniffer.start(device_name, self._on_packet, ""):
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
            self.stop_btn.configure(state="normal")
            self._update_status("抓包中...")
        else:
            messagebox.showerror("错误", "启动抓包失败！\n请确保：\n1. 已正确安装 Npcap\n2. 以管理员权限运行\n3. 检查控制台日志")

    def _toggle_pause(self):
        """
        切换暂停状态
        """
        if self.sniffer.is_running:
            # 这里我们只是简单地改变按钮文字
            # 实际的暂停功能可以后续实现
            if self.pause_btn.cget("text") == "暂停":
                self.pause_btn.configure(text="继续")
                self._update_status("已暂停")
            else:
                self.pause_btn.configure(text="暂停")
                self._update_status("抓包中...")

    def _stop_capture(self):
        """
        停止抓包
        """
        self.sniffer.stop()
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled", text="暂停")
        self.stop_btn.configure(state="disabled")
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
        # 检查是否超过最大包数
        if len(self.packet_list.all_packets) >= self.max_packets:
            # 移除最早的包
            self.packet_list.all_packets.pop(0)
        
        self.packet_list.add_packet(packet)
        self._update_status()
        self._update_stats()

    def _on_packet_select(self, packet):
        """
        数据包选择回调
        """
        self.packet_detail.display_packet(packet)

    def _apply_filter(self):
        """
        应用过滤
        """
        enabled = self.enable_filter_var.get()
        protocol = self.protocol_combo.get()
        
        # 解析端口
        ports = set()
        port_text = self.port_entry.get().strip()
        if port_text:
            for p in port_text.split(','):
                try:
                    port = int(p.strip())
                    if 0 < port < 65536:
                        ports.add(port)
                except ValueError:
                    pass
        
        self.packet_list.set_filter(enabled, ports, protocol)
        self._update_status()

    def _clear_filter(self):
        """
        清空过滤
        """
        self.port_entry.delete(0, "end")
        self.protocol_combo.set("全部")
        self.enable_filter_var.set(False)
        self._apply_filter()

    def _update_max_packets(self):
        """
        更新最大包数
        """
        try:
            self.max_packets = int(self.max_packets_combo.get())
        except ValueError:
            self.max_packets = 5000

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
        packets = self.packet_list.all_packets
        if not packets:
            messagebox.showwarning("警告", "没有可保存的数据包")
            return

        ExportManager.save_pcap(packets)

    def _update_status(self, text=None):
        """
        更新状态
        """
        total_count = self.packet_list.get_packet_count()
        displayed_count = self.packet_list.get_displayed_count()
        
        if text:
            self.status_label.configure(
                text=f"{text} - 总包数: {total_count}/{self.max_packets}, 显示: {displayed_count}"
            )
        else:
            if self.sniffer.is_running:
                status_text = "抓包中..."
            else:
                status_text = "就绪"
            self.status_label.configure(
                text=f"{status_text} - 总包数: {total_count}/{self.max_packets}, 显示: {displayed_count}"
            )

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
