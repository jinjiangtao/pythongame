
"""
数据包详情组件
显示选中数据包的详细信息
"""

import customtkinter as ctk
from tkinter import ttk
from utils import format_hex_dump


class PacketDetail(ctk.CTkFrame):
    """
    数据包详情组件
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        """
        创建界面组件
        """
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(tree_frame, text="协议树").pack(pady=2)
        self.tree = ttk.Treeview(tree_frame)
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        hex_frame = ctk.CTkFrame(self)
        hex_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(hex_frame, text="十六进制数据").pack(pady=2)
        self.hex_text = ctk.CTkTextbox(hex_frame, font=("Consolas", 10))
        self.hex_text.pack(fill="both", expand=True)

    def display_packet(self, packet):
        """
        显示数据包详情
        """
        self._clear_tree()

        tree_data = packet.get_tree_data()
        for section_name, items in tree_data:
            section_id = self.tree.insert("", "end", text=section_name, open=True)
            for item in items:
                self.tree.insert(section_id, "end", text=item)

        hex_dump = format_hex_dump(packet.raw_data)
        self.hex_text.delete("1.0", "end")
        self.hex_text.insert("1.0", "\n".join(hex_dump))

    def _clear_tree(self):
        """
        清空协议树
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear(self):
        """
        清空所有内容
        """
        self._clear_tree()
        self.hex_text.delete("1.0", "end")
