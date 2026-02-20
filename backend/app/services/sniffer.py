from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
import pandas as pd
from datetime import datetime
import threading
import logging

class PacketSniffer:
    def __init__(self, callback_func=None):
        self.callback_func = callback_func
        self.is_sniffing = False
        self.packet_count = 0
        self.flow_data = {} # To track flow duration

    def extract_features(self, packet):
        """
        Extracts 1️⃣ Packet Capture Module features:
        Source IP, Destination IP, Protocol, Packet Length, Flags, Timestamp, Flow Duration.
        """
        try:
            if not packet.haslayer(IP):
                return None

            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            pkt_len = len(packet)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Flags extraction (TCP only)
            flags = ""
            if packet.haslayer(TCP):
                flags = str(packet[TCP].flags)
            elif packet.haslayer(UDP):
                flags = "UDP"
            elif packet.haslayer(ICMP):
                flags = "ICMP"

            # Simple Flow Duration logic (Simplified for initial version)
            flow_key = f"{src_ip}-{dst_ip}-{proto}"
            current_time = time.time()
            if flow_key not in self.flow_data:
                self.flow_data[flow_key] = current_time
                flow_duration = 0
            else:
                flow_duration = current_time - self.flow_data[flow_key]

            feature_dict = {
                "timestamp": timestamp,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": proto,
                "length": pkt_len,
                "flags": flags,
                "flow_duration": round(flow_duration, 4),
                "payload": bytes(packet)[:64].hex() # Capture first 64 bytes for Hex View
            }
            
            return feature_dict
        except Exception as e:
            logging.error(f"Error extracting features: {e}")
            return None

    def process_packet(self, packet):
        if not self.is_sniffing:
            return

        features = self.extract_features(packet)
        if features and self.callback_func:
            self.packet_count += 1
            self.callback_func(features)

    def stop_sniffing_filter(self, packet):
        return not self.is_sniffing

    def start_sniffing(self, interface=None):
        self.is_sniffing = True
        
        try:
            # Check if Scapy can actually sniff on Windows
            from scapy.config import conf
            import scapy.arch.windows
            
            # Simple check for Npcap/WinPcap on Windows
            print(f"[*] Starting network sniffer on {interface or 'default interface'}...")
            
            sniff_thread = threading.Thread(
                target=sniff, 
                kwargs={
                    "prn": self.process_packet, 
                    "iface": interface, 
                    "store": False,
                    "stop_filter": self.stop_sniffing_filter
                },
                daemon=True
            )
            sniff_thread.start()
            
            # Brief wait to see if thread crashes immediately
            time.sleep(1)
            if not sniff_thread.is_alive():
                raise RuntimeError("Sniffer thread died immediately. Check pcap installation.")

        except Exception as e:
            print(f"[!] SCAPY ERROR: {e}")
            print("[!] libpcap/Npcap not found. Switching to MOCK SIMULATION MODE.")
            self.start_mock_sniffing()

    def start_mock_sniffing(self):
        """Generates fake packets if real sniffing is unavailable."""
        def mock_loop():
            import random
            ips = [
                "192.168.1.15", "10.0.0.4", "172.16.0.5", "185.25.12.4", "45.33.22.11", 
                "8.8.8.8", "1.1.1.1", "SAT_NODE_ALPHA", "SAT_NODE_BRAVO"
            ]
            while self.is_sniffing:
                src = random.choice(ips)
                protocol = "SAT" if "SAT" in src else random.choice(["TCP", "UDP", "ICMP"])
                
                fake_packet = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "src_ip": src,
                    "dst_ip": "192.168.1.1",
                    "protocol": protocol,
                    "length": random.randint(40, 4096) if protocol == "SAT" else random.randint(40, 1500),
                    "flags": "UPLINK" if protocol == "SAT" else random.choice(["SF", "S0", "REJ"]),
                    "flow_duration": round(random.uniform(0.1, 2.0), 4)
                }
                if self.callback_func:
                    self.callback_func(fake_packet)
                time.sleep(random.uniform(0.05, 0.2)) # Much faster generation
        
        threading.Thread(target=mock_loop, daemon=True).start()

    def stop_sniffing(self):
        self.is_sniffing = False
        print("[*] Sniffer stopped.")

# Example usage (standalone)
if __name__ == "__main__":
    def print_callback(features):
        print(f"Captured: {features}")

    sniffer = PacketSniffer(callback_func=print_callback)
    sniffer.start_sniffing()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sniffer.stop_sniffing()
