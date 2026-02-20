import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import psutil
import time
from datetime import datetime
from typing import List

from .services.sniffer import PacketSniffer
from .services.preprocessor import Preprocessor
from .services.ml_engine import MLEngine
from .services.dl_engine import DLDetector
from .services.utils import GeoLocator, Retrainer, FirewallManager, OSINTChecker, ForensicRecorder, XAIEngine, PredictiveEngine, LLMAnalyzer
from .services.chatbot import SecurityAssistant
from .services.honeypot import HoneypotSystem
from .services.ledger import ImmutableLedger
from .services.notifications import TelegramSOC

app = FastAPI(title="Quantum AI IDS: God Mode V2")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

preprocessor = Preprocessor(); ml_engine = MLEngine(); dl_detector = DLDetector()
geolocator = GeoLocator(); firewall = FirewallManager(); osint = OSINTChecker()
forensics = ForensicRecorder(); ledger = ImmutableLedger(); telegram_soc = TelegramSOC()
xai = XAIEngine(); predictor = PredictiveEngine(); llm = LLMAnalyzer()

sniffer = None
honeypot = None

stats = {
    "total_packets": 0, "total_attacks": 0, "live_feed": [],
    "attack_distribution": {"DoS": 0, "Probe": 0, "Brute Force": 0, "R2L": 0, "U2R": 0, "Zero-Day": 0, "Honeypot": 0},
    "is_active": False, "auto_block": False, "defcon": 5,
    "system_health": {"cpu": 0, "ram": 0}, "ledger_integrity": not ledger.is_compromised,
    "honeypot_hits": 0, "forecast": [], "raw_hex_stream": "",
    "topology": {"nodes": [], "links": []}, # 🕸️ Graph Data
    "kill_switch_engaged": False
}

def set_defcon_level(level): stats["defcon"] = level
assistant = SecurityAssistant(firewall_ref=firewall, osint_ref=osint, ledger_ref=ledger, stats_ref=stats, set_defcon_func=set_defcon_level)
manager_ws = []

async def broadcast_stats():
    while True:
        if manager_ws:
            stats["system_health"] = {"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent}
            stats["forecast"] = predictor.predict_next_10_mins()
            
            # 🕸️ Generate Graph Topology (Simulated Relation)
            nodes = [{"id": "HQ", "group": 1, "size": 20}]
            links = []
            seen_ips = set()
            for p in stats["live_feed"][:15]: # Last 15 packets
                if p["src_ip"] not in seen_ips:
                    nodes.append({"id": p["src_ip"], "group": 2 if p["status"] == "DANGEROUS" else 3, "size": 10})
                    seen_ips.add(p["src_ip"])
                links.append({"source": p["src_ip"], "target": "HQ", "value": 1})
            
            stats["topology"] = {"nodes": nodes, "links": links}

            msg = json.dumps(stats)
            for ws in list(manager_ws): # Use list() to create a copy for iteration
                try: await ws.send_text(msg)
                except: 
                    if ws in manager_ws:
                        manager_ws.remove(ws)
        await asyncio.sleep(0.1)

@app.on_event("startup")
async def startup(): asyncio.create_task(broadcast_stats())

def process_packet_callback(packet):
    global stats
    if stats["kill_switch_engaged"]: return # 🚨 KILL SWITCH ACTIVE

    stats["raw_hex_stream"] = f"{packet.get('src_ip')} > {packet.get('dst_ip')} | {packet.get('payload', '00')[:32]}"
    vector = preprocessor.preprocess_live_data(packet)
    is_honeypot = packet.get("is_honeypot_hit", False)
    
    if is_honeypot:
        res = {"prediction": "Attack", "attack_type": "Honeypot", "confidence": 1.0}
        stats["honeypot_hits"] += 1
    else:
        res = ml_engine.predict(vector)
        is_ano, score = dl_detector.detect_anomaly(vector)
        if is_ano and res["prediction"] == "Normal":
            res = {"prediction": "Attack", "attack_type": "Zero-Day", "confidence": 0.99}

    stats["total_packets"] += 1
    predictor.update(res["prediction"] == "Attack")

    status_label = "NORMAL"
    if res["prediction"] == "Attack":
        status_label = "DANGEROUS"
        stats["total_attacks"] += 1
        stats["attack_distribution"][res["attack_type"]] += 1
    elif res["confidence"] > 0.90:
        status_label = "SAFE"

    # OSINT & Risk Score with Breakdown
    reputation = 0
    if status_label == "DANGEROUS" or stats["total_packets"] % 10 == 0:
        reputation = osint.check_reputation(packet["src_ip"])
    
    risk_val, breakdown = preprocessor.get_risk_score(res["confidence"], res["attack_type"], reputation)
    
    # 🧠 LLM Analysis
    llm_report = llm.analyze_payload({"risk_score": risk_val})

    packet_entry = {
        "timestamp": packet["timestamp"], "src_ip": packet["src_ip"], "dst_ip": packet.get("dst_ip", "LOCAL"),
        "status": status_label, "attack_type": res["attack_type"], "risk_score": risk_val,
        "risk_breakdown": breakdown, # 🚀 NEW: Mathematical breakdown
        "payload": packet.get("payload", ""), "reasons": xai.explain(packet, res["attack_type"]),
        "reputation": reputation, "geo": geolocator.get_location(packet["src_ip"]),
        "llm_analysis": llm_report # 🧠 AI Insight
    }

    stats["live_feed"] = ([packet_entry] + stats["live_feed"])[:20]

    if status_label == "DANGEROUS":
        if stats["auto_block"] and risk_val > 8: firewall.block_ip(packet["src_ip"])
        ledger.add_entry(f"Event: {res['attack_type']} from {packet['src_ip']}")

@app.post("/api/start")
async def start():
    print("[*] API: /api/start called.")
    global sniffer, honeypot
    if stats["is_active"]:
        return {"status": "Already running"}
        
    stats["is_active"] = True
    stats["kill_switch_engaged"] = False # Reset on start
    
    print("[*] Starting sniffer...")
    if sniffer is None:
        sniffer = PacketSniffer(callback_func=process_packet_callback)
    sniffer.start_sniffing()
    
    print("[*] Starting honeypot...")
    if honeypot is None:
        honeypot = HoneypotSystem(callback_func=process_packet_callback)
    honeypot.start()
    
    print("[*] API: /api/start finished.")
    return {"status": "Engaged"}

@app.post("/api/stop")
async def stop():
    print("[*] API: /api/stop called.")
    global sniffer, honeypot
    stats["is_active"] = False
    if sniffer: 
        sniffer.stop_sniffing()
    if honeypot: 
        honeypot.stop()
    return {"status": "Offline"}

@app.post("/api/killswitch")
async def killswitch():
    print("🚨 KILL SWITCH ACTIVATED")
    stats["kill_switch_engaged"] = True
    stats["is_active"] = False
    global sniffer, honeypot
    if sniffer: sniffer.stop_sniffing()
    if honeypot: honeypot.stop()
    return {"status": "SYSTEM_SEVERED"}

@app.post("/api/reset-killswitch")
async def reset_killswitch():
    print("♻️ KILL SWITCH RESET")
    stats["kill_switch_engaged"] = False
    return {"status": "SYSTEM_RESTORED"}

@app.post("/api/set-defcon")
async def set_defcon(l: dict): 
    stats["defcon"] = l.get("level", 5)
    return {"status": "OK", "level": stats["defcon"]}

@app.post("/api/toggle-autoblock")
async def toggle_ab(): 
    stats["auto_block"] = not stats["auto_block"]
    return {"status": "OK", "auto_block": stats["auto_block"]}

@app.websocket("/ws/stats")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    manager_ws.append(ws)
    try:
        while True: 
            data = await ws.receive_text()
    except WebSocketDisconnect:
        if ws in manager_ws:
            manager_ws.remove(ws)
    except Exception:
        if ws in manager_ws:
            manager_ws.remove(ws)

@app.post("/api/chat")
async def chat(q: dict): 
    return {"reply": assistant.get_response(q.get("message", ""))}

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000)

