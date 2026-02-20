import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

class Preprocessor:
    def __init__(self, model_dir="models/"):
        self.model_dir = model_dir
        self.scaler = StandardScaler()
        self.protocol_encoder = LabelEncoder()
        self.flag_encoder = LabelEncoder()
        self.protocols = ["tcp", "udp", "icmp"]
        self.flags = ["SF", "S0", "REJ", "RSTR", "RSTO", "SH", "S1", "S2", "RSTOS0", "S3", "OTH"]
        self.load_transformers()

    def save_transformers(self):
        if not os.path.exists(self.model_dir): os.makedirs(self.model_dir)
        joblib.dump(self.scaler, os.path.join(self.model_dir, "scaler.pkl"))
        joblib.dump(self.protocol_encoder, os.path.join(self.model_dir, "protocol_encoder.pkl"))
        joblib.dump(self.flag_encoder, os.path.join(self.model_dir, "flag_encoder.pkl"))

    def load_transformers(self):
        try:
            self.scaler = joblib.load(os.path.join(self.model_dir, "scaler.pkl"))
            self.protocol_encoder = joblib.load(os.path.join(self.model_dir, "protocol_encoder.pkl"))
            self.flag_encoder = joblib.load(os.path.join(self.model_dir, "flag_encoder.pkl"))
        except:
            self.protocol_encoder.fit(self.protocols + ["unknown"])
            self.flag_encoder.fit(self.flags + ["unknown"])

    def preprocess_live_data(self, packet_features):
        protocol_val = str(packet_features["protocol"]).lower()
        if protocol_val not in self.protocols: protocol_val = "unknown"
        protocol_encoded = self.protocol_encoder.transform([protocol_val])[0]
        vector = np.array([packet_features["flow_duration"], protocol_encoded, packet_features["length"], 0, 0, 0, 0, 0, 0, 0]).reshape(1, -1)
        return vector

    def get_risk_score(self, confidence, attack_type, reputation=0):
        """
        🚀 GOD-MODE SCORING ENGINE
        Returns (final_score, breakdown_dict)
        """
        base_weights = {
            "Normal": 1.0,
            "DoS": 8.5,
            "Probe": 5.0,
            "Brute Force": 9.0,
            "R2L": 7.5,
            "U2R": 9.5,
            "Zero-Day": 8.0,
            "Honeypot": 10.0
        }
        
        base = base_weights.get(attack_type, 1.0)
        
        # Factor 1: Probabilistic Weight (Severity * Confidence)
        prob_score = base * confidence
        
        # Factor 2: OSINT Modifier (Global Reputation)
        osint_mod = (reputation / 100) * 1.5 # Max +1.5 boost for bad rep
        
        final_score = prob_score + osint_mod
        final_score = round(min(10, max(0.1, final_score)), 1)
        
        breakdown = {
            "base_severity": base,
            "confidence": round(confidence * 100, 1),
            "osint_impact": round(osint_mod, 2),
            "formula": f"({base} * {round(confidence, 2)}) + {round(osint_mod, 2)}"
        }
        
        return final_score, breakdown
