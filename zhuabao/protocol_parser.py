
"""
协议解析器
解析以太网帧、IP、TCP、UDP、ARP、ICMP等协议
"""

import struct
from settings import ETHER_TYPE_IP, ETHER_TYPE_ARP, IP_PROTO_ICMP, IP_PROTO_TCP, IP_PROTO_UDP
from utils import mac_to_str, ip_to_str


class Packet:
    """
    数据包类，存储解析后的数据包信息
    """
    def __init__(self, raw_data, timestamp):
        self.raw_data = raw_data
        self.timestamp = timestamp
        self.length = len(raw_data)
        self.ethernet = None
        self.ip = None
        self.tcp = None
        self.udp = None
        self.icmp = None
        self.arp = None
        self.protocol = "UNKNOWN"
        self.src_ip = ""
        self.dst_ip = ""
        self.src_port = ""
        self.dst_port = ""
        self.summary = ""
        self.parse()

    def parse(self):
        """
        解析数据包
        """
        self.parse_ethernet()

    def parse_ethernet(self):
        """
        解析以太网帧
        """
        eth_length = 14
        eth_header = self.raw_data[:eth_length]
        eth = struct.unpack('!6s6sH', eth_header)

        self.ethernet = {
            'dst_mac': mac_to_str(eth[0]),
            'src_mac': mac_to_str(eth[1]),
            'type': eth[2]
        }

        if eth[2] == ETHER_TYPE_IP:
            self.parse_ip(eth_length)
        elif eth[2] == ETHER_TYPE_ARP:
            self.parse_arp(eth_length)
        else:
            self.protocol = "OTHER"
            self.summary = f"Ethernet: {self.ethernet['src_mac']} -&gt; {self.ethernet['dst_mac']}"

    def parse_ip(self, offset):
        """
        解析IP头部
        """
        ip_header = self.raw_data[offset:offset + 20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        version = version_ihl &gt;&gt; 4
        ihl = version_ihl &amp; 0xF
        iph_length = ihl * 4

        self.ip = {
            'version': version,
            'ihl': ihl,
            'tos': iph[1],
            'total_len': iph[2],
            'id': iph[3],
            'flags_frag': iph[4],
            'ttl': iph[5],
            'protocol': iph[6],
            'checksum': iph[7],
            'src_ip': ip_to_str(iph[8]),
            'dst_ip': ip_to_str(iph[9])
        }

        self.src_ip = self.ip['src_ip']
        self.dst_ip = self.ip['dst_ip']

        if iph[6] == IP_PROTO_TCP:
            self.parse_tcp(offset + iph_length)
        elif iph[6] == IP_PROTO_UDP:
            self.parse_udp(offset + iph_length)
        elif iph[6] == IP_PROTO_ICMP:
            self.parse_icmp(offset + iph_length)
        else:
            self.protocol = f"IP-{iph[6]}"
            self.summary = f"IP: {self.src_ip} -&gt; {self.dst_ip}"

    def parse_tcp(self, offset):
        """
        解析TCP头部
        """
        tcp_header = self.raw_data[offset:offset + 20]
        tcph = struct.unpack('!HHLLBBHHH', tcp_header)

        data_offset_reserved = tcph[4]
        tcph_length = (data_offset_reserved &gt;&gt; 4) * 4

        self.tcp = {
            'src_port': tcph[0],
            'dst_port': tcph[1],
            'seq': tcph[2],
            'ack': tcph[3],
            'data_offset': data_offset_reserved &gt;&gt; 4,
            'reserved': data_offset_reserved &amp; 0xF,
            'flags': tcph[5],
            'window': tcph[6],
            'checksum': tcph[7],
            'urg_ptr': tcph[8]
        }

        self.protocol = "TCP"
        self.src_port = str(tcph[0])
        self.dst_port = str(tcph[1])

        if tcph[1] == 80 or tcph[0] == 80:
            self.protocol = "HTTP"
        elif tcph[1] == 443 or tcph[0] == 443:
            self.protocol = "HTTPS"

        self.summary = f"TCP: {self.src_ip}:{self.src_port} -&gt; {self.dst_ip}:{self.dst_port}"

    def parse_udp(self, offset):
        """
        解析UDP头部
        """
        udp_header = self.raw_data[offset:offset + 8]
        udph = struct.unpack('!HHHH', udp_header)

        self.udp = {
            'src_port': udph[0],
            'dst_port': udph[1],
            'length': udph[2],
            'checksum': udph[3]
        }

        self.protocol = "UDP"
        self.src_port = str(udph[0])
        self.dst_port = str(udph[1])
        self.summary = f"UDP: {self.src_ip}:{self.src_port} -&gt; {self.dst_ip}:{self.dst_port}"

    def parse_icmp(self, offset):
        """
        解析ICMP头部
        """
        icmp_header = self.raw_data[offset:offset + 4]
        icmph = struct.unpack('!BBH', icmp_header)

        self.icmp = {
            'type': icmph[0],
            'code': icmph[1],
            'checksum': icmph[2]
        }

        self.protocol = "ICMP"
        self.summary = f"ICMP: {self.src_ip} -&gt; {self.dst_ip} Type={icmph[0]}"

    def parse_arp(self, offset):
        """
        解析ARP数据包
        """
        arp_header = self.raw_data[offset:offset + 28]
        arph = struct.unpack('!HHBBH6s4s6s4s', arp_header)

        self.arp = {
            'hw_type': arph[0],
            'proto_type': arph[1],
            'hw_size': arph[2],
            'proto_size': arph[3],
            'opcode': arph[4],
            'sender_mac': mac_to_str(arph[5]),
            'sender_ip': ip_to_str(arph[6]),
            'target_mac': mac_to_str(arph[7]),
            'target_ip': ip_to_str(arph[8])
        }

        self.protocol = "ARP"
        self.src_ip = self.arp['sender_ip']
        self.dst_ip = self.arp['target_ip']

        if arph[4] == 1:
            self.summary = f"ARP Request: Who has {self.dst_ip}? Tell {self.src_ip}"
        elif arph[4] == 2:
            self.summary = f"ARP Reply: {self.src_ip} is at {self.arp['sender_mac']}"
        else:
            self.summary = f"ARP: {self.src_ip} -&gt; {self.dst_ip}"

    def get_tree_data(self):
        """
        获取协议树数据，用于显示
        """
        tree = []
        tree.append(("Frame", [f"Length: {self.length} bytes"]))

        if self.ethernet:
            eth_items = [
                f"Destination: {self.ethernet['dst_mac']}",
                f"Source: {self.ethernet['src_mac']}",
                f"Type: 0x{self.ethernet['type']:04x}"
            ]
            tree.append(("Ethernet", eth_items))

        if self.ip:
            ip_items = [
                f"Version: {self.ip['version']}",
                f"Header Length: {self.ip['ihl'] * 4} bytes",
                f"Total Length: {self.ip['total_len']}",
                f"TTL: {self.ip['ttl']}",
                f"Protocol: {self.ip['protocol']}",
                f"Source: {self.ip['src_ip']}",
                f"Destination: {self.ip['dst_ip']}"
            ]
            tree.append(("IP", ip_items))

        if self.tcp:
            tcp_items = [
                f"Source Port: {self.tcp['src_port']}",
                f"Destination Port: {self.tcp['dst_port']}",
                f"Sequence Number: {self.tcp['seq']}",
                f"Acknowledgment: {self.tcp['ack']}",
                f"Header Length: {self.tcp['data_offset'] * 4} bytes",
                f"Flags: 0x{self.tcp['flags']:02x}"
            ]
            tree.append(("TCP", tcp_items))

        if self.udp:
            udp_items = [
                f"Source Port: {self.udp['src_port']}",
                f"Destination Port: {self.udp['dst_port']}",
                f"Length: {self.udp['length']}",
                f"Checksum: 0x{self.udp['checksum']:04x}"
            ]
            tree.append(("UDP", udp_items))

        if self.icmp:
            icmp_items = [
                f"Type: {self.icmp['type']}",
                f"Code: {self.icmp['code']}",
                f"Checksum: 0x{self.icmp['checksum']:04x}"
            ]
            tree.append(("ICMP", icmp_items))

        if self.arp:
            arp_op = "Request" if self.arp['opcode'] == 1 else "Reply"
            arp_items = [
                f"Hardware Type: {self.arp['hw_type']}",
                f"Protocol Type: 0x{self.arp['proto_type']:04x}",
                f"Opcode: {self.arp['opcode']} ({arp_op})",
                f"Sender MAC: {self.arp['sender_mac']}",
                f"Sender IP: {self.arp['sender_ip']}",
                f"Target MAC: {self.arp['target_mac']}",
                f"Target IP: {self.arp['target_ip']}"
            ]
            tree.append(("ARP", arp_items))

        return tree
