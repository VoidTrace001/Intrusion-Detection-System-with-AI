# AI-Powered Intrusion Detection System (IDS) 🛡️

An advanced, real-time Network Intrusion Detection System using Machine Learning (Random Forest) and FastAPI.

## 🔥 Advanced Features Added
- **1️⃣ WebSocket**: Real-time push updates for the dashboard.
- **2️⃣ Geo-location**: Mapping source IPs to physical cities and countries.
- **3️⃣ Admin Auth**: JWT-based authentication system for system controls.
- **4️⃣ Model Retraining**: Module to refresh models using historical traffic data.
- **5️⃣ Docker Deployment**: Fully containerized setup via `docker-compose`.

---

## 🐋 Docker Setup
Run the entire stack (Backend + Frontend) in one command:
```bash
docker-compose up --build
```
*Note: Docker needs elevated privileges for packet capture on the host network.*

---

## 🛠️ Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
```

### 2. Network Sniffing Requirements (Windows)
For live packet capture, you **must** have **Npcap** installed (installed by default with Wireshark).
[Download Npcap here](https://npcap.com/#download).

### 3. Train the Models
Generate the ML models using the provided script (uses synthetic data if dataset download fails).
```bash
python data/train_ids_models.py
```

### 4. Run the Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 5. Run the Frontend (Optional - requires Node.js)
```bash
cd frontend
npm install
npm start
```
*Alternatively, you can access the API directly at `http://localhost:8000/docs`.*

---

## 📂 Project Structure
- `backend/app/main.py`: FastAPI server and IDS logic.
- `backend/app/services/`: Core logic (Sniffer, ML Engine, Preprocessor).
- `models/`: Saved `.pkl` model files.
- `data/`: Training scripts and datasets.
- `frontend/src/`: React dashboard code.

## 🧪 Simulation Mode
If you cannot capture live traffic, use the simulation script to feed dummy packets into the system:
```bash
python data/simulate_traffic.py
```
