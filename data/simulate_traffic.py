import requests
import time
import random
from datetime import datetime

# IDS Backend URL
URL = "http://localhost:8000/api/stats" # Note: This script simulates by feeding data directly to the callback if imported, or by mimicking the data flow.

# For this demo, let's create a script that triggers the internal callback of the backend 
# if the backend is running.

def simulate_traffic():
    print("[*] Starting Traffic Simulation...")
    print("[*] Sending packets to IDS logic (simulated)...")
    
    ips = ["192.168.1.10", "10.0.0.5", "172.16.0.2", "8.8.8.8", "192.168.0.100"]
    protocols = ["TCP", "UDP", "ICMP"]
    
    while True:
        src = random.choice(ips)
        dst = random.choice(ips)
        if src == dst: continue
        
        # Simulate a packet
        packet = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": src,
            "dst_ip": dst,
            "protocol": random.choice(protocols),
            "length": random.randint(40, 1500),
            "flags": random.choice(["SF", "S0", "REJ", "UDP", "ICMP"]),
            "flow_duration": round(random.uniform(0.1, 5.0), 4)
        }
        
        # In a real environment, the sniffer would call the backend logic.
        # Since this is a separate script, we'll just show what the data looks like.
        print(f"[*] Simulated Packet: {packet['src_ip']} -> {packet['dst_ip']} ({packet['protocol']})")
        
        # To truly simulate, you'd want to call the internal processing logic 
        # or have an endpoint that accepts external packets for analysis.
        
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    try:
        simulate_traffic()
    except KeyboardInterrupt:
        print("\n[*] Simulation stopped.")
