
"""
抓包核心引擎
使用pcap-ct进行网络数据包捕获
"""

import threading
import time
import pcap
from protocol_parser import Packet


class Sniffer:
    """
    抓包器类
    """

    def __init__(self):
        self.is_running = False
        self.capture_thread = None
        self.pcap_obj = None
        self.packet_callback = None
        self.current_device = None
        self.devices = []
        self.load_devices()

    def load_devices(self):
        """
        加载可用网卡列表
        """
        try:
            self.devices = pcap.findalldevs()
        except Exception as e:
            print(f"加载网卡失败: {e}")
            self.devices = []

    def get_devices(self):
        """
        获取可用网卡列表
        """
        return self.devices

    def start(self, device_name, callback, bpf_filter=""):
        """
        开始抓包
        """
        if self.is_running:
            return False

        self.current_device = device_name
        self.packet_callback = callback

        try:
            self.pcap_obj = pcap.pcap(name=device_name, promisc=True, timeout_ms=50)
            if bpf_filter:
                self.pcap_obj.setfilter(bpf_filter)

            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            return True
        except Exception as e:
            print(f"启动抓包失败: {e}")
            return False

    def _capture_loop(self):
        """
        抓包循环，在单独线程中运行
        """
        try:
            for timestamp, raw_data in self.pcap_obj:
                if not self.is_running:
                    break
                packet = Packet(raw_data, timestamp)
                if self.packet_callback:
                    self.packet_callback(packet)
        except Exception as e:
            if self.is_running:
                print(f"抓包过程出错: {e}")
        finally:
            self.is_running = False

    def stop(self):
        """
        停止抓包
        """
        self.is_running = False
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        if self.pcap_obj:
            try:
                self.pcap_obj.close()
            except:
                pass
            self.pcap_obj = None
