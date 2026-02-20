import socket
import threading
import time
from datetime import datetime

class HoneypotSystem:
    def __init__(self, callback_func=None):
        self.callback_func = callback_func
        self.ghost_ports = [22, 23, 3306, 21, 5900] # SSH, Telnet, MySQL, FTP, VNC
        self.is_running = False
        self.threads = []

    def _listen_on_port(self, port):
        """Creates a 'Ghost' listener that traps anyone who connects."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(('0.0.0.0', port))
                s.listen(5)
                s.settimeout(1.0) # 1 second timeout for accept()
                print(f"[*] Honeypot: Ghost Port {port} is now LIVE and waiting for traps.")
                
                while self.is_running:
                    try:
                        client_sock, addr = s.accept()
                    except socket.timeout:
                        continue
                    
                    with client_sock:
                        src_ip = addr[0]
                        print(f"[!] TRAP: Intruder from {src_ip} touched Ghost Port {port}!")
                        
                        # Trigger immediate high-risk alert
                        if self.callback_func:
                            trap_data = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "src_ip": src_ip,
                                "dst_ip": "HONEYPOT",
                                "protocol": "TCP",
                                "length": 0,
                                "flags": "TRAP",
                                "flow_duration": 0,
                                "is_honeypot_hit": True,
                                "attack_type": "Honeypot Trap",
                                "risk_score": 10.0,
                                "confidence": 1.0
                            }
                            self.callback_func(trap_data)
                        
                        # 🕸️ TARPIT MODE: Engage Sticky Defense
                        # Keep connection open but waste their time
                        try:
                            client_sock.sendall(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\n")
                            for _ in range(5):
                                if not self.is_running: break
                                time.sleep(2) # Waste 2 seconds
                                client_sock.sendall(b".") # Keep alive
                        except:
                            pass
            except Exception as e:
                print(f"[!] Honeypot Error on port {port}: {e}")

    def start(self):
        self.is_running = True
        for port in self.ghost_ports:
            t = threading.Thread(target=self._listen_on_port, args=(port,), daemon=True)
            t.start()
            self.threads.append(t)

    def stop(self):
        self.is_running = False
        print("[*] Honeypot System Offline.")
