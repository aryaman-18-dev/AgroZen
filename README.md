# 🌱 AgriTech — Smart Farming Solutions

![AgriTech Banner](images/plant.png)

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Application Preview](#️-application-preview)
- [System Architecture](#-system-architecture)
- [Core Features](#-core-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Backend vs Frontend](#backend-vs-frontend)
- [Security & Reliability](#-security--reliability)
- [Environment Variables](#️-environment-variables)
- [Roadmap](#-roadmap)
- [Production Deployment](#-production-deployment)
- [API Keys Guide](#-api-keys-guide)
- [FAQ](#-faq)

---

> ⚠️ **Note:** For production deployment, use a WSGI server like `gunicorn` instead of Flask's built-in server.

> ⚠️ **Never commit your `.env` file or API keys to the repository. Always keep secrets private!**

---

**AgriTech** is an AI-powered smart agriculture platform designed to assist farmers with crop
recommendations, yield prediction, plant disease detection, and community-driven collaboration—enabling sustainable and data-driven farming practices.

---

## 📌 Overview

- AI-driven decision support for modern agriculture
- Early-stage plant disease detection
- Crop yield forecasting using machine learning models
- Collaborative ecosystem for farmers and stakeholders

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aryaman-18-dev/AgriTech.git
cd AgriTech
```

### 2️⃣ Create a Python virtual environment (Windows PowerShell)

Run these commands from the project root. Using the virtual environment keeps this
project's packages separate from other Python installations:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, use
`.\.venv\Scripts\python.exe -m pip ...` for package commands and
`.\.venv\Scripts\python.exe app.py` to start the app.

Create a private `.env` file from the template if you do not already have one:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Edit `.env` and fill in keys for the integrations you plan to use. Optional integrations
such as Gemini, Firebase, SMTP, and external data services remain unavailable until
their credentials are configured. Never commit `.env` or share its values.

### 3️⃣ Start the Application

From the project root, run:

```powershell
python app.py
```

Keep this PowerShell window open. A successful start displays
`Running on http://127.0.0.1:5000` and does not return to the PowerShell prompt.
The entry point starts one Socket.IO server without Flask's Windows debug reloader.

Open the website at:

```text
http://127.0.0.1:5000/
```

Flask serves the main `index.html` from the repository root along with the backend
routes, so a separate static frontend server is not needed. The `src/frontend` folder
contains feature components and pages, not the main homepage.

**Backend health and port check**

Open `http://127.0.0.1:5000/health` in your browser. In a second PowerShell window,
you can check that the server is listening with:

```powershell
Test-NetConnection 127.0.0.1 -Port 5000
```

It should report `TcpTestSucceeded : True`. If it reports `False`, verify that the
first PowerShell window is still running `python app.py` and has not returned to its
prompt or printed a traceback.

If crop recommendations say no active model version is configured, migrate the
existing crop model once from the project root, then restart the app:

```powershell
python -m backend.ml_models.migrate_models --migrate-crop
```

---

## 🖥️ Application Preview

<img src="images/image1.png"
       alt="AgriTech Dashboard" width="100%" />
<img src="images/image.png"
       alt="AgriTech Dashboard" width="100%" />

<img src="images/image2.png"
       alt="AgriTech Dashboard" width="100%" />
<img src="images/image3.png"
       alt="AgriTech Dashboard" width="100%" />

---

## 🏗️ System Architecture

1. **User Input:** Soil data and plant images
2. **Backend Processing:** Flask APIs and model routing
3. **ML Inference:**
   - CNNs for disease detection
   - Random Forest / XGBoost for crop recommendation
   - Regression models for yield prediction
4. **Output:** Predictions with insights and actions

---

## 🌟 Core Features

- 🌾 Crop Recommendation
- 🌿 Fertilizer Recommendation
- 📉 Yield Prediction
- 🔬 Disease Detection
- � **AI Chatbot** - Platform guidance & agriculture support
- �🤝 Farmer Community
- 🛒 Shopkeeper Listings

---

## 🤖 AI Chatbot

AgriTech's AI-powered chatbot provides comprehensive support for farmers:

### Features

- **Platform Guidance**: Explains how to use all AgriTech features and tools
- **Agriculture Support**: Answers farming questions, crop recommendations, pest control
- **Decision Making**: Provides region-specific, season-based farming advice
- **Image Analysis**: Upload plant photos for disease detection and diagnosis
- **24/7 Support**: Always available for instant farming assistance

### Technical Implementation

- **Dual Mode**: AI-powered (Google Gemini) + Rule-based fallback
- **Smart Matching**: Fuzzy search with keyword analysis for accurate responses
- **Offline Capability**: Works without internet using JSON-based responses
- **Image Processing**: Analyzes plant photos for disease identification

### Usage

```bash
# Start the chatbot server
npm install
node server.js

# Access at: http://localhost:3000/chat
```

### API Endpoints

- `POST /api/chat` - Send messages and images for AI analysis

---

## 🛠️ Tech Stack

### 🎨 Frontend

- HTML5
- CSS3
- JavaScript (ES6)

### ⚙️ Backend

- Python (Flask)
- Node.js (Optional)

### 🤖 Machine Learning

- TensorFlow
- Scikit-learn
- OpenCV

### 🗄️ Database & DevOps

- MySQL
- MongoDB
- Firebase
- Docker
- GitHub Actions

---

## 📂 Project Structure

```text
AGRITECH/
├── app.py                      # 🐍 Flask Backend (Main entry point)
├── server.js                   # 🟢 Node.js Chatbot Server
├── package.json                # Node.js dependencies
├── requirements.txt            # Python dependencies
├── firebase.js                 # Firebase config fetching
├── 📁 chatbot/
│   ├── chat.html               # 🤖 Chatbot interface
│   ├── chat.js                 # Chatbot client logic
│   ├── chat.css                # Chatbot styling
│   ├── json-chatbot.js         # Rule-based chatbot engine
│   └── chatbot-responses.json  # Predefined responses
├── 📁 src/
│   └── 📁 frontend/            # 🌐 Frontend UI (HTML, CSS, JS)
│       ├── 📁 pages/           # Individual page files
│       ├── 📁 css/             # Stylesheets
│       └── 📁 js/              # Client-side scripts
├── 📁 Crop Recommendation/   # 🌾 Crop recommendation module
├── 📁 Fertiliser Recommendation System/   # 🌿 Fertilizer recommendation ML module
├── 📁 Disease Prediction/     # 🔬 Disease detection module
├── 📁 Crop Yield Prediction/   # 📊 Yield forecasting module
├── 📁 Community/               # 💬 community/forum backend
├── 📁 images/                  # 📸 Screenshots and assets
├── 📄 README.md                # This file
└── 📄 CONTRIBUTING.md          # Contribution guidelines
```

---

### Backend vs Frontend

- **Backend** (`app.py` at root): Flask server handling APIs, Firebase config
- **Frontend** (`src/frontend/`): Static HTML/CSS/JS served via Python HTTP server
- **Optional Node Server** (`server.js`): Alternative chat backend (not required)

---

## 🔐 Security & Reliability

- Image sanitization using OpenCV
- Secrets stored in `.env` files
- ML models evaluated using standard performance metrics (accuracy varies by model and dataset)

---

### ⚙️ Environment Variables

```bash
GEMINI_API_KEY=your_api_key
FIREBASE_API_KEY=your_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_bucket.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
```

---

## 🔐 Registration Validation Rules

To maintain clean user data and enforce business policies, AgriTech now applies strict
validation whenever a new account is created (frontend **and** backend):

- **Full Name / Username:** only alphabetic characters and spaces are allowed. The
  same rule is enforced in the database model, API routes, and client-side form.
- **Email:** registrations are limited to `@gmail.com` addresses. Non‑Gmail domains
  are rejected both on the client and by API endpoints.

Error messages are shown immediately on the form and the backend returns a descriptive
400 response when validation fails. Automated tests cover both model‑level and
endpoint behavior.

---

---

## 🛣️ Roadmap

- Cloud Deployment
- Mobile Application
- Real-Time Weather API
- ~~AI Chatbot~~ ✅ **COMPLETED**
- Multilingual Support

---

---

## 🔑 API Keys Guide

- **Gemini API Key:** [Google AI Studio](https://aistudio.google.com/) se generate karein.
- **Firebase Keys:** [Firebase Console](https://console.firebase.google.com/) se apne project ke liye keys lein.
- API keys ko `.env` file me store karein (kabhi bhi repo me commit na karein).

---

## 🛠️ Common Issues & Fixes

- ❌ **ModuleNotFoundError**
  👉 Run `pip install -r requirements.txt`

- ❌ **Firebase config error**
  👉 Ensure `.env` values match Firebase Console

- ❌ **CORS issue**
  👉 Make sure backend runs before frontend

- ❌ **Port already in use**
  👉 Change port in `app.py` or stop previous process

## ❓ FAQ

**Q: The project is not running. What should I do?**
A: Make sure all Python dependencies are installed, the .env file is properly configured, and the correct API keys are being used.

**Q: How do I get a Gemini/Firebase API key?**
A: Refer to the “API Keys Guide” section above for step-by-step instructions.

**Q: I am seeing the warning “This is a development server…” on the Flask server. What does it mean?**
A: This server is intended only for development. For production, use a WSGI server such as Gunicorn.

**Q: I accidentally pushed my .env file. What should I do?**
A: Immediately rotate/regenerate your API keys, remove the .env file from Git tracking, add it to .gitignore, and clean the repository history if required.

**Q: The /health endpoint is not responding. What could be wrong?**
A: Ensure the backend server is running correctly and that the /health route is properly implemented.

---

**Made with ❤️ by the AgriTech Community — 2026**
