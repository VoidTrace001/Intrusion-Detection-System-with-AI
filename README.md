# 🛡️ AI-Powered Intrusion Detection System (IDS)

> A real-time, full-stack Network Intrusion Detection System powered by Machine Learning — built with FastAPI, React, WebSockets, and Docker.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

This project is a production-grade **AI-powered Intrusion Detection System** that monitors network traffic in real time, classifies malicious activity using a trained machine learning model, and alerts administrators through a live web dashboard.

Built as a full-stack application with a **Python/FastAPI backend**, **React frontend**, **JWT-secured admin panel**, and full **Docker containerization** — this system is designed to reflect how real-world security infrastructure operates.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **ML-Based Detection** | Trained model classifies network packets as normal or attack traffic |
| ⚡ **Real-Time Alerts** | WebSocket-powered live dashboard with instant threat notifications |
| 🌍 **IP Geolocation** | Maps source IPs to physical cities and countries on detection |
| 🔐 **JWT Authentication** | Secure admin login system to protect system controls |
| 🔁 **Model Retraining** | Built-in module to retrain the model on new historical traffic data |
| 🐳 **Docker Deployment** | Full stack containerized via `docker-compose` — runs in one command |
| 🧪 **Simulation Mode** | Feed synthetic attack traffic without needing live network access |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      React Frontend                      │
│         (Live Dashboard + Alerts + Admin Panel)          │
└─────────────────────────┬───────────────────────────────┘
                          │  REST API + WebSocket
┌─────────────────────────▼───────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  ML Engine  │  │ Packet       │  │  JWT Auth     │  │
│  │  (Predict)  │  │ Sniffer      │  │  Middleware   │  │
│  └──────┬──────┘  └──────┬───────┘  └───────────────┘  │
│         │                │                               │
│  ┌──────▼──────┐  ┌──────▼───────┐                      │
│  │ Preprocessor│  │ Geo-location │                      │
│  └─────────────┘  └──────────────┘                      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              SQLite Database (Event Logs)                │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Intrusion-Detection-System-with-AI/
│
├── backend/
│   └── app/
│       ├── main.py               # FastAPI server + IDS core logic
│       └── services/
│           ├── sniffer.py        # Live packet capture (Scapy)
│           ├── ml_engine.py      # ML model inference
│           └── preprocessor.py  # Feature extraction & normalization
│
├── frontend/
│   └── src/                     # React dashboard
│
├── models/                      # Saved .pkl model files
├── data/
│   ├── train_ids_models.py      # Model training script
│   └── simulate_traffic.py      # Traffic simulation for testing
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── test_ws.py                   # WebSocket connection tests
```

---

## 🚀 Quick Start

### Option 1 — Docker (Recommended)

```bash
git clone https://github.com/VoidTrace001/Intrusion-Detection-System-with-AI.git
cd Intrusion-Detection-System-with-AI
docker-compose up --build
```

> ⚠️ Docker requires elevated (root/admin) privileges for live packet capture.

Access the dashboard at: `http://localhost:3000`  
API docs at: `http://localhost:8000/docs`

---

### Option 2 — Manual Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Windows users: Install Npcap** (required for live packet capture)  
→ [Download Npcap](https://npcap.com/#download) *(installed by default with Wireshark)*

**3. Train the ML model**
```bash
python data/train_ids_models.py
```

**4. Start the backend**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**5. Start the frontend** *(requires Node.js)*
```bash
cd frontend
npm install
npm start
```

**Or** access the API directly via Swagger UI at `http://localhost:8000/docs`

---

### 🧪 Simulation Mode

No live network? No problem. Run the simulation script to feed synthetic attack traffic:

```bash
python data/simulate_traffic.py
```

---

## 🤖 ML Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Dataset | NSL-KDD / Synthetic traffic data |
| Input Features | Packet headers, protocol type, service, flags, byte counts |
| Output Classes | `Normal`, `DoS`, `Probe`, `R2L`, `U2R` |
| Model Format | `.pkl` (scikit-learn) |

The model is trained via `data/train_ids_models.py` and supports **live retraining** through the admin panel to adapt to evolving network behavior.

---

## 🔐 Security Features

- **JWT Authentication** — All admin endpoints require a signed token
- **Role-based access** — Separation between read-only monitoring and system controls
- **Geolocation of threats** — Source IPs are resolved to city/country on every alert
- **Event logging** — All detections are persisted in a local database for audit trails

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Admin login, returns JWT token |
| `GET` | `/api/alerts` | Fetch recent intrusion alerts |
| `GET` | `/api/stats` | Traffic statistics and model metrics |
| `POST` | `/api/retrain` | Trigger model retraining |
| `WS` | `/ws/alerts` | WebSocket stream for live alerts |

Full interactive API documentation: `http://localhost:8000/docs`

---

## 🧰 Tech Stack

**Backend:** Python, FastAPI, Scapy, scikit-learn, WebSockets, JWT, SQLite  
**Frontend:** React, JavaScript, CSS  
**DevOps:** Docker, docker-compose  

---

## ⚠️ Disclaimer

This tool is developed strictly for **educational and authorized security research purposes**. Using this software to monitor networks without explicit permission is illegal. The author takes no responsibility for misuse.

---

## 📄 Documentation

- 📘 [Technical Report (PDF)](./Quantum_AI_IDS_Technical_Report.pdf) — In-depth breakdown of the system architecture, ML pipeline, and threat classification methodology
- 📋 [Detailed Report](./REPORT.md)

---

## 👤 Author ##

**VoidTrace001**  
🔗 [GitHub Profile](https://github.com/VoidTrace001)

---

*If you found this project useful, consider leaving a ⭐ — it helps others find it!*
