
"""
导出功能
保存和加载pcap文件
"""

import struct
import time
from tkinter import filedialog, messagebox


class ExportManager:
    """
    导出管理器
    """

    @staticmethod
    def save_pcap(packets, filename=None):
        """
        保存为pcap文件
        """
        if not filename:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pcap",
                filetypes=[("PCAP文件", "*.pcap"), ("所有文件", "*.*")]
            )
            if not filename:
                return False

        try:
            with open(filename, 'wb') as f:
                f.write(ExportManager._get_pcap_header())
                for packet in packets:
                    f.write(ExportManager._get_pcap_record(packet))
            return True
        except Exception as e:
            messagebox.showerror("保存失败", f"保存PCAP文件出错: {e}")
            return False

    @staticmethod
    def _get_pcap_header():
        """
        生成pcap文件头
        """
        magic = 0xa1b2c3d4
        version_major = 2
        version_minor = 4
        thiszone = 0
        sigfigs = 0
        snaplen = 65535
        network = 1
        return struct.pack('IHHiIII', magic, version_major, version_minor,
                           thiszone, sigfigs, snaplen, network)

    @staticmethod
    def _get_pcap_record(packet):
        """
        生成pcap记录
        """
        ts_sec = int(packet.timestamp)
        ts_usec = int((packet.timestamp - ts_sec) * 1000000)
        incl_len = len(packet.raw_data)
        orig_len = incl_len
        return struct.pack('IIII', ts_sec, ts_usec, incl_len, orig_len) + packet.raw_data
