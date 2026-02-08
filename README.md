# 🔍 Lucid TRACE
### Technological Review of Artificial Content in Evidence

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

**Lucid TRACE** is a forensic video analysis tool designed to verify the authenticity of digital evidence. It uses a **FastAPI** backend to extract frames and run AI detection (via Sightengine/TruthScan), and a **React** frontend to provide a clean, user-friendly interface for investigators.

---

## 🚀 Key Features

* **Full-Stack Architecture:** Decoupled React frontend and Python backend for scalability.
* **Stochastic Sampling:** Extracts random frames to prevent temporal overfitting.
* **Dual-Metric Analysis:** Calculates both **Average Confidence** and **Max Spike** to catch subtle deepfake edits.
* **Evidence Hashing:** Generates SHA-256 hashes for chain-of-custody verification.

---

## 🛠️ Installation & Setup

### **1. Backend (Python/FastAPI)**

1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Start the Server:**
    * *Standard Command:*
        ```bash
        uvicorn main:app --reload
        ```
    * *If "uvicorn" is not recognized (Windows):*
        ```bash
        python -m uvicorn main:app --reload
        ```
    The API will start at: `http://127.0.0.1:8000`

### **2. Frontend (React/Vite)**

1.  Open a new terminal and navigate to the frontend folder:
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  **Start the UI:**
    ```bash
    npm run dev
    ```
    Open your browser to the link provided (usually `http://localhost:5173`).

---

## 📂 Project Structure

```text
lucid-trace/
├── backend/                 # Python Logic
│   ├── main.py              # API Entry Point
│   ├── video_processor.py   # OpenCV Frame Extraction
│   ├── detector.py          # AI Detection Logic
│   └── requirements.txt     # Python Dependencies
└── frontend/                # React UI
    ├── src/
    │   ├── App.jsx          # Main Interface
    │   └── App.css          # Dark Mode Styling
    └── package.json         # Node Dependencies