"""
主窗口界面
整合所有组件，支持暂停/继续、实时过滤、自动滚屏、包数量限制
"""

import customtkinter as ctk
from tkinter import messagebox
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, APPEARANCE_MODE, MAX_PACKET_OPTIONS
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
        self.current_bpf_filter = ""
        self._setup_window()
        self._create_widgets()
        self._load_devices()
        self._update_button_states()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_window(self):
        """
        设置窗口
        """
        ctk.set_appearance_mode(APPEARANCE_MODE)
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def _create_widgets(self):
        """
        创建界面组件
        """
        # 第一行：网卡选择 + 控制按钮
        top_frame1 = ctk.CTkFrame(self)
        top_frame1.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(top_frame1, text="网卡:").pack(side="left", padx=5)
        self.device_combo = ctk.CTkComboBox(top_frame1, values=[], state="readonly", width=400)
        self.device_combo.pack(side="left", padx=5)
        
        self.start_btn = ctk.CTkButton(top_frame1, text="开始抓包", command=self._start_capture)
        self.start_btn.pack(side="left", padx=5)
        
        self.pause_btn = ctk.CTkButton(top_frame1, text="暂停", command=self._toggle_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(top_frame1, text="停止", command=self._stop_capture, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(top_frame1, text="清空列表", command=self._clear_list)
        self.clear_btn.pack(side="left", padx=5)
        
        self.save_btn = ctk.CTkButton(top_frame1, text="保存PCAP", command=self._save_pcap)
        self.save_btn.pack(side="left", padx=5)
        
        # 第二行：过滤器
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        self.filter_manager = FilterManager(filter_frame, self._on_filter_change, self._on_bpf_filter_change)
        self.filter_manager.pack(fill="x", expand=True)
        
        # 第三行：自动滚屏 + 最大包数 + 状态栏
        top_frame2 = ctk.CTkFrame(self)
        top_frame2.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        self.auto_scroll_check = ctk.CTkCheckBox(top_frame2, text="自动滚屏", variable=self.auto_scroll_var, command=self._on_auto_scroll_change)
        self.auto_scroll_check.pack(side="left", padx=5)
        
        ctk.CTkLabel(top_frame2, text="最大包数:").pack(side="left", padx=5)
        
        self.max_packets_combo = ctk.CTkComboBox(top_frame2, values=MAX_PACKET_OPTIONS, state="readonly", width=100)
        self.max_packets_combo.set("10000")
        self.max_packets_combo.pack(side="left", padx=5)
        self.max_packets_combo.bind("<<ComboboxSelected>>", lambda e: self._on_max_packets_change())
        
        # 状态栏
        self.status_label = ctk.CTkLabel(top_frame2, text="就绪 - 已捕获: 0 个包")
        self.status_label.pack(side="left", padx=20)
        
        self.stats_label = ctk.CTkLabel(top_frame2, text="")
        self.stats_label.pack(side="right", padx=5)
        
        # 数据包列表
        self.packet_list = PacketList(self, self._on_packet_select)
        self.packet_list.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        
        # 数据包详情
        self.packet_detail = PacketDetail(self)
        self.packet_detail.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

    def _load_devices(self):
        """
        加载网卡列表，显示友好名称
        """
        devices = self.sniffer.get_devices()
        self.device_map = {}  # 保存显示名和实际名的映射
        display_names = []
        
        for dev in devices:
            desc = self.sniffer.device_descriptions.get(dev, "")
            if desc:
                display_name = f"{desc} - {dev}"
            else:
                display_name = dev
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

    def _update_button_states(self):
        """
        更新按钮状态
        """
        is_running = self.sniffer.is_running
        is_paused = self.sniffer.is_paused
        
        if not is_running:
            # 未抓包状态
            self.start_btn.configure(state="normal", text="开始抓包")
            self.pause_btn.configure(state="disabled", text="暂停")
            self.stop_btn.configure(state="disabled")
            self.device_combo.configure(state="readonly")
            self.clear_btn.configure(state="normal")
        elif is_paused:
            # 暂停状态
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal", text="继续")
            self.stop_btn.configure(state="normal")
            self.device_combo.configure(state="disabled")
            self.clear_btn.configure(state="normal")
        else:
            # 抓包状态
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal", text="暂停")
            self.stop_btn.configure(state="normal")
            self.device_combo.configure(state="disabled")
            self.clear_btn.configure(state="disabled")

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

        if self.sniffer.start(device_name, self._on_packet, self.current_bpf_filter):
            self._update_button_states()
            self._update_status("正在捕获...")
            # 重置用户滚动标志
            self.packet_list.user_scrolled = False
        else:
            messagebox.showerror("错误", "启动抓包失败！\n请确保：\n1. 已正确安装 Npcap\n2. 以管理员权限运行\n3. 检查控制台日志")

    def _toggle_pause(self):
        """
        切换暂停/继续
        """
        if self.sniffer.is_paused:
            self.sniffer.resume()
            self.packet_list.user_scrolled = False
        else:
            self.sniffer.pause()
        self._update_button_states()
        self._update_status()

    def _stop_capture(self):
        """
        停止抓包
        """
        self.sniffer.stop()
        self._update_button_states()
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

    def _on_filter_change(self, enabled, protocol, ports):
        """
        过滤器变化回调
        """
        self.packet_list.set_filter(enabled, protocol, ports)
        self._update_status()

    def _on_bpf_filter_change(self, filter_str):
        """
        BPF过滤器变化回调
        """
        self.current_bpf_filter = filter_str
        if self.sniffer.is_running:
            messagebox.showinfo("提示", "BPF过滤器将在下次开始抓包时生效")

    def _on_auto_scroll_change(self):
        """
        自动滚屏开关变化
        """
        self.packet_list.set_auto_scroll(self.auto_scroll_var.get())

    def _on_max_packets_change(self):
        """
        最大包数变化
        """
        self.packet_list.set_max_packets(self.max_packets_combo.get())

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
        total_count = self.packet_list.get_packet_count()
        displayed_count = self.packet_list.get_displayed_count()
        max_packets = self.max_packets_combo.get()
        
        status_text = ""
        if text:
            status_text = f"{text} - "
        elif self.sniffer.is_paused:
            status_text = "已暂停 - "
        elif self.sniffer.is_running:
            status_text = "正在捕获 - "
        else:
            status_text = "就绪 - "
        
        max_info = f"/{max_packets}" if max_packets != "不限" else ""
        
        if displayed_count != total_count:
            status_text += f"已捕获: {total_count}{max_info} 个包 (显示: {displayed_count})"
        else:
            status_text += f"已捕获: {total_count}{max_info} 个包"
        
        self.status_label.configure(text=status_text)

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
