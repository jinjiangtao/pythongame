"""
过滤器管理
提供协议过滤、端口过滤、过滤开关和BPF过滤器
"""

import customtkinter as ctk
from settings import PROTOCOL_OPTIONS


class FilterManager(ctk.CTkFrame):
    """
    过滤器管理组件
    """

    def __init__(self, parent, on_filter_change, on_bpf_filter_change=None):
        super().__init__(parent)
        self.on_filter_change = on_filter_change
        self.on_bpf_filter_change = on_bpf_filter_change
        self._create_widgets()

    def _create_widgets(self):
        """
        创建界面组件
        """
        # 第一行：协议过滤
        row1 = ctk.CTkFrame(self)
        row1.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row1, text="协议过滤:").pack(side="left", padx=5)
        
        self.protocol_combo = ctk.CTkComboBox(row1, values=PROTOCOL_OPTIONS, state="readonly", width=100)
        self.protocol_combo.set("全部")
        self.protocol_combo.pack(side="left", padx=5)
        self.protocol_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())
        
        ctk.CTkLabel(row1, text="端口过滤:").pack(side="left", padx=5)
        
        self.port_entry = ctk.CTkEntry(row1, placeholder_text="80,443,8080", width=150)
        self.port_entry.pack(side="left", padx=5)
        self.port_entry.bind("<KeyRelease>", lambda e: self._apply_filter())
        self.port_entry.bind("<Return>", lambda e: self._apply_filter())
        
        self.enable_filter = ctk.BooleanVar(value=False)
        self.filter_check = ctk.CTkCheckBox(row1, text="启用过滤", variable=self.enable_filter, command=self._apply_filter)
        self.filter_check.pack(side="left", padx=5)
        
        ctk.CTkButton(row1, text="清空过滤", command=self._clear_filter, width=80).pack(side="left", padx=5)
        
        # 第二行：BPF过滤器（保留原有功能）
        row2 = ctk.CTkFrame(self)
        row2.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row2, text="BPF过滤器:").pack(side="left", padx=5)
        
        self.bpf_filter_entry = ctk.CTkEntry(row2, placeholder_text="例如: tcp port 80")
        self.bpf_filter_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.bpf_filter_entry.bind("<Return>", lambda e: self._apply_bpf_filter())
        
        bpf_btn_frame = ctk.CTkFrame(row2)
        bpf_btn_frame.pack(side="left", padx=5)
        
        ctk.CTkButton(bpf_btn_frame, text="仅TCP", command=lambda: self._set_bpf_filter("tcp"), width=60).pack(side="left", padx=2)
        ctk.CTkButton(bpf_btn_frame, text="仅UDP", command=lambda: self._set_bpf_filter("udp"), width=60).pack(side="left", padx=2)
        ctk.CTkButton(bpf_btn_frame, text="仅HTTP", command=lambda: self._set_bpf_filter("tcp port 80"), width=60).pack(side="left", padx=2)
        ctk.CTkButton(bpf_btn_frame, text="清空", command=lambda: self._set_bpf_filter(""), width=60).pack(side="left", padx=2)

    def _set_bpf_filter(self, filter_str):
        """
        设置BPF过滤器
        """
        self.bpf_filter_entry.delete(0, "end")
        self.bpf_filter_entry.insert(0, filter_str)
        self._apply_bpf_filter()

    def _apply_bpf_filter(self):
        """
        应用BPF过滤器
        """
        if self.on_bpf_filter_change:
            self.on_bpf_filter_change(self.bpf_filter_entry.get())

    def _clear_filter(self):
        """
        清空所有过滤条件
        """
        self.protocol_combo.set("全部")
        self.port_entry.delete(0, "end")
        self.enable_filter.set(False)
        self._apply_filter()

    def _apply_filter(self):
        """
        应用过滤条件
        """
        if self.on_filter_change:
            self.on_filter_change(
                enabled=self.enable_filter.get(),
                protocol=self.protocol_combo.get(),
                ports=self.port_entry.get()
            )

    def get_bpf_filter(self):
        """
        获取当前BPF过滤器
        """
        return self.bpf_filter_entry.get()
