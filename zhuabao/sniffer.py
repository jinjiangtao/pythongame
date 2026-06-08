"""
抓包核心引擎
使用pcap-ct进行网络数据包捕获，修复API调用问题
"""

import threading
import time
import socket
import re
import pcap
from protocol_parser import Packet

try:
    import winreg
    HAS_WINREG = True
except ImportError:
    HAS_WINREG = False


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
        self.device_info = {}  # 存储设备完整信息 (friendly_name, ip_addresses, is_connected)
        self.load_devices()

    def load_devices(self):
        """
        加载可用网卡列表，增强对设备信息的获取
        """
        try:
            all_devices = pcap.findalldevs()
            self.devices = []
            self.device_info = {}
            
            # 为每个设备尝试获取更详细信息
            for dev in all_devices:
                self.devices.append(dev)
                self.device_info[dev] = self._get_device_info(dev)
            
            # 打印调试信息
            print(f"发现 {len(self.devices)} 个网络设备:")
            for i, dev in enumerate(self.devices):
                info = self.device_info.get(dev, {})
                print(f"  [{i}] {dev} -> {info}")
                
        except Exception as e:
            print(f"加载网卡失败: {e}")
            import traceback
            traceback.print_exc()
            self.devices = []

    def _extract_guid(self, device_name):
        """
        从设备名称中提取 GUID
        """
        # 匹配类似 {12345678-1234-1234-1234-123456789ABC} 的 GUID
        match = re.search(r'\{[0-9A-Fa-f-]+\}', device_name)
        if match:
            return match.group(0)
        return None

    def _get_device_info(self, device_name):
        """
        获取设备的完整信息，包括友好名称和IP地址
        """
        info = {
            'friendly_name': '',
            'ip_addresses': [],
            'is_connected': False
        }
        
        # 尝试从 Windows 注册表获取友好名称
        if HAS_WINREG:
            guid = self._extract_guid(device_name)
            if guid:
                try:
                    # 打开注册表路径
                    network_key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        r"SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}"
                    )
                    
                    try:
                        # 打开 GUID 对应的子键
                        guid_key = winreg.OpenKey(network_key, guid)
                        try:
                            # 打开 Connection 子键
                            connection_key = winreg.OpenKey(guid_key, "Connection")
                            try:
                                # 读取 Name 字段
                                name, _ = winreg.QueryValueEx(connection_key, "Name")
                                info['friendly_name'] = name
                            finally:
                                winreg.CloseKey(connection_key)
                        except FileNotFoundError:
                            pass
                        finally:
                            winreg.CloseKey(guid_key)
                    except FileNotFoundError:
                        pass
                    finally:
                        winreg.CloseKey(network_key)
                except Exception as e:
                    print(f"读取注册表失败: {e}")
        
        # 如果注册表获取失败，尝试简单匹配
        if not info['friendly_name']:
            device_lower = device_name.lower()
            if "loopback" in device_lower:
                info['friendly_name'] = "Loopback (本地回环)"
            elif "wlan" in device_lower or "wifi" in device_lower or "wi-fi" in device_lower:
                info['friendly_name'] = "WLAN"
            elif "ethernet" in device_lower or "eth" in device_lower:
                info['friendly_name'] = "以太网"
            elif "npf" in device_lower:
                info['friendly_name'] = "本地连接"
            else:
                info['friendly_name'] = device_name
        
        # 尝试获取 IP 地址
        try:
            # 简单的方法：获取本地所有 IP 地址，但无法精确对应到网卡
            # 这里我们可以后续改进，暂时标记为已连接
            info['is_connected'] = True
        except:
            pass
        
        return info

    def get_devices(self):
        """
        获取可用网卡列表
        """
        return self.devices

    def start(self, device_name, callback, bpf_filter=""):
        """
        开始抓包，使用正确的 pcap-ct API
        """
        if self.is_running:
            return False

        self.current_device = device_name
        self.packet_callback = callback

        try:
            print(f"正在打开设备: {device_name}")
            
            # 打开设备，使用标准参数
            self.pcap_obj = pcap.pcap(
                name=device_name,
                promisc=True,
                timeout_ms=100
            )
            
            if bpf_filter:
                try:
                    print(f"应用过滤器: {bpf_filter}")
                    self.pcap_obj.setfilter(bpf_filter)
                except Exception as fe:
                    print(f"过滤器设置失败: {fe}")
                    # 忽略过滤器错误，继续抓包

            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            print("抓包已启动")
            return True
        except Exception as e:
            print(f"启动抓包失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _capture_loop(self):
        """
        抓包循环，使用正确的迭代方式
        """
        packet_count = 0
        print("抓包循环开始")
        try:
            # 使用正确的迭代方式获取数据包
            for timestamp, raw_data in self.pcap_obj:
                if not self.is_running:
                    break
                
                packet_count += 1
                # 每10个包打印一次，避免刷屏
                if packet_count % 10 == 0:
                    print(f"已捕获 {packet_count} 个包")
                
                try:
                    packet = Packet(raw_data, timestamp)
                    if self.packet_callback:
                        self.packet_callback(packet)
                except Exception as pe:
                    print(f"解析数据包异常: {pe}")
                    
        except StopIteration:
            print("抓包迭代器结束")
        except Exception as e:
            if self.is_running:
                print(f"抓包过程出错: {e}")
                import traceback
                traceback.print_exc()
        finally:
            self.is_running = False
            print(f"抓包循环结束，共捕获 {packet_count} 个包")

    def stop(self):
        """
        停止抓包
        """
        print("正在停止抓包...")
        self.is_running = False
        if self.capture_thread and self.capture_thread.is_alive():
            try:
                self.capture_thread.join(timeout=2.0)  # 增加等待时间
            except:
                pass
        if self.pcap_obj:
            try:
                self.pcap_obj.close()
            except:
                pass
            self.pcap_obj = None
        print("抓包已停止")
