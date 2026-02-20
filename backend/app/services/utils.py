import requests
import joblib
import os
import threading
import time
import scapy.all as scapy
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import numpy as np

class XAIEngine:
    """Explainable AI: Why did the model flag this?"""
    def explain(self, features, attack_type):
        reasons = []
        
        # Heuristic Reasoning (Rapid-XAI)
        if features['length'] > 1000:
            reasons.append("Abnormal Payload Size (>1KB)")
        elif features['length'] < 20:
            reasons.append("Suspiciously Small Packet (Probe)")
            
        if features['flow_duration'] > 1.0:
            reasons.append("Long Flow Duration (Persistence)")
            
        if features['protocol'] == 17: # UDP
            reasons.append("UDP Flood Signature")
        elif features['protocol'] == 6 and 'S' in str(features.get('flags', '')):
            reasons.append("TCP SYN Anomalies")
            
        if attack_type == "Honeypot":
            reasons = ["Unauthorized Access to Ghost Port", "Trap Triggered"]
            
        if not reasons:
            reasons.append("Statistical Deviation from Baseline")
            
        return reasons

class PredictiveEngine:
    """Time-Series Forecasting for Threat Levels."""
    def __init__(self):
        self.history = [] # Stores counts per minute
        self.last_tick = time.time()
        self.current_minute_count = 0

    def update(self, is_attack):
        if is_attack:
            self.current_minute_count += 1
            
        # Tick every 10 seconds for smoothness
        if time.time() - self.last_tick > 10:
            self.history.append(self.current_minute_count)
            self.current_minute_count = 0
            self.last_tick = time.time()
            if len(self.history) > 60: self.history.pop(0)

    def predict_next_10_mins(self):
        if not self.history: return [0]*10
        avg = sum(self.history) / len(self.history)
        trend = (self.history[-1] - self.history[0]) / len(self.history) if len(self.history) > 1 else 0
        
        # Simple Linear Projection
        forecast = []
        current = self.history[-1]
        for i in range(10):
            current += trend
            forecast.append(max(0, round(current + avg * 0.1, 1)))
        return forecast

class OSINTChecker:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.cache = {}

    def check_reputation(self, ip):
        if ip.startswith(("192.168", "127.0.0", "10.", "172.")): return 0
        if ip in self.cache: return self.cache[ip]
        if not self.api_key:
            import random
            score = random.randint(0, 100) if random.random() > 0.8 else 0
            self.cache[ip] = score
            return score
        return 0

class ForensicRecorder:
    def __init__(self, output_dir="data/forensics/"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)

    def save_evidence(self, packet_features, attack_type):
        filename = f"evidence_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{attack_type}.txt"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(f"EVIDENCE REPORT: {attack_type}\n")
            f.write(f"PAYLOAD: {packet_features.get('payload', 'N/A')}\n")
        return path

class FirewallManager:
    def __init__(self): self.blocked_ips = {}
    def block_ip(self, ip, duration_minutes=60): pass
    def cleanup_expired_bans(self): pass

class GeoLocator:
    def __init__(self):
        self.cache = {
            "8.8.8.8": {"city": "Mountain View", "country": "USA", "lat": 37.422, "lon": -122.084},
            "1.1.1.1": {"city": "Sydney", "country": "Australia", "lat": -33.868, "lon": 151.209},
            "192.168.1.15": {"city": "Local Node", "country": "Internal", "lat": 34.052, "lon": -118.243},
            "10.0.0.4": {"city": "Private Cloud", "country": "VPN", "lat": 51.507, "lon": -0.127},
            "172.16.0.5": {"city": "Datacenter Alpha", "country": "Germany", "lat": 50.110, "lon": 8.682},
            "185.25.12.4": {"city": "Moscow", "country": "Russia", "lat": 55.755, "lon": 37.617},
            "45.33.22.11": {"city": "Tokyo", "country": "Japan", "lat": 35.689, "lon": 139.692},
            "SAT_NODE_ALPHA": {"city": "Low Earth Orbit", "country": "SAT_LINK", "lat": 0, "lon": -45}, # Atlantic
            "SAT_NODE_BRAVO": {"city": "Geostationary", "country": "SAT_LINK", "lat": 0, "lon": 160}   # Pacific
        }

    def get_location(self, ip):
        if ip in self.cache:
            return self.cache[ip]
        
        # Simulated global distribution for unknown IPs
        import random
        return {
            "city": "Unknown Remote",
            "country": "OSINT Target",
            "lat": random.uniform(-60, 60),
            "lon": random.uniform(-180, 180)
        }

class Retrainer:
    def __init__(self): pass

class LLMAnalyzer:
    """Simulates a Local LLM analyzing packet payloads for semantic threats."""
    def analyze_payload(self, packet):
        import random
        threats = [
            "SQL Injection attempt detected in payload body.",
            "Potential Buffer Overflow: NOP sled pattern identified.",
            "Cross-Site Scripting (XSS) vector found in URI.",
            "Command Injection: Shell metacharacters detected.",
            "Suspicious encoded Shellcode signature."
        ]
        
        if packet.get("risk_score", 0) > 7:
            return {
                "analysis": random.choice(threats),
                "confidence": round(random.uniform(0.85, 0.99), 2),
                "model": "Llama-3-8B-Quantized"
            }
        return {
            "analysis": "Traffic appears benign. No semantic anomalies.",
            "confidence": 0.99,
            "model": "Llama-3-8B-Quantized"
        }
