
"""
过滤器管理
提供BPF过滤器快捷按钮和输入框
"""

import customtkinter as ctk


class FilterManager(ctk.CTkFrame):
    """
    过滤器管理组件
    """

    def __init__(self, parent, on_filter_change):
        super().__init__(parent)
        self.on_filter_change = on_filter_change
        self._create_widgets()

    def _create_widgets(self):
        """
        创建界面组件
        """
        ctk.CTkLabel(self, text="过滤器 (BPF):").pack(side="left", padx=5)

        self.filter_entry = ctk.CTkEntry(self, placeholder_text="例如: tcp port 80")
        self.filter_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.filter_entry.bind("&lt;Return&gt;", lambda e: self._apply_filter())

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="仅TCP", command=lambda: self._set_filter("tcp"), width=60).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="仅UDP", command=lambda: self._set_filter("udp"), width=60).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="仅HTTP", command=lambda: self._set_filter("tcp port 80"), width=60).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="清空", command=lambda: self._set_filter(""), width=60).pack(side="left", padx=2)

    def _set_filter(self, filter_str):
        """
        设置过滤器
        """
        self.filter_entry.delete(0, "end")
        self.filter_entry.insert(0, filter_str)
        self._apply_filter()

    def _apply_filter(self):
        """
        应用过滤器
        """
        filter_str = self.filter_entry.get()
        if self.on_filter_change:
            self.on_filter_change(filter_str)

    def get_filter(self):
        """
        获取当前过滤器
        """
        return self.filter_entry.get()
