# AI Voice-to-Text Task Manager using AWS 🎙️⚡

An intelligent, full-stack, cloud-native task management web application powered by **Python (Flask)**, **Amazon S3**, **Amazon Transcribe**, **Amazon EC2**, and **Natural Language Processing (NLP)**.

Users speak tasks naturally (e.g. *"Remind me to submit my Python assignment tomorrow at 5 PM. It is very important."*), and the application converts spoken speech into text, extracts task attributes (Title, Date, Time, Priority, Urgency, Category), presents a confirmation preview, and manages tasks on a modern cosmic dashboard.

---

## 🌟 Key Features

- 🎙️ **Voice Task Creation**: Browser microphone capture using standard `MediaRecorder API` with 60-second limit and live timer.
- 🤖 **AI Task Understanding (NLP)**: Automatic extraction of:
  - **Title & Description**
  - **Relative & Absolute Dates** (e.g., *today*, *tomorrow*, *next Monday*) resolved against configured timezone (`Asia/Kolkata`)
  - **Target Time** (24-hour formatted string like `17:00`)
  - **Priority System** (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`)
  - **Urgency System** (`URGENT` / `NORMAL`)
  - **Auto-Categorization** (`College`, `Study`, `Work`, `Shopping`, `Health`, `Finance`, `Meeting`, `Personal`, `Other`)
- 👁️ **Task Confirmation Modal**: Interactive preview step to review and edit extracted details before saving.
- 📊 **Dynamic Cosmic Dashboard**: Real-time stats (`Total`, `Pending`, `Completed`, `Urgent`, `Overdue`), full-text search, quick filters, and complete CRUD operations.
- ☁️ **AWS Cloud Architecture**: Integrates Amazon S3 for audio storage, Amazon Transcribe for ASR, and IAM roles for least-privilege security. Includes seamless local development fallback mode.

---

## 🏗️ Architecture Overview

```
User (Browser) ──► HTML5 / Vanilla JS Dashboard
                         │
                         ▼ (POST /api/transcribe Audio Blob)
                  Flask API Backend (Python)
                         │
       ┌─────────────────┴─────────────────┐
       ▼                                   ▼
 [ Amazon S3 ]                    [ Amazon Transcribe ]
  (Audio Upload)                  (Speech Recognition)
       │                                   │
       └─────────────────┬─────────────────┘
                         ▼
             [ AI Task Parser Engine ]
         (NLP Date & Attribute Extraction)
                         │
                         ▼
            [ Task Preview Modal Window ]
                         │
                         ▼ (POST /api/tasks)
            [ Task Service & SQLite DB ]
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ installed on your system.

### 1. Clone & Set Up Backend

```bash
cd backend

# Create Python Virtual Environment (Optional)
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:

```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=dev-secret-key-voice-ai-task-manager-2026
TIMEZONE=Asia/Kolkata
AWS_REGION=ap-south-1
S3_BUCKET_NAME=voice-task-manager-audio-bucket
MAX_AUDIO_SIZE_MB=10
UPLOAD_FOLDER=uploads
```

### 3. Run the Flask Server

```bash
python app.py
```
The server will start at `http://127.0.0.1:5000`.

### 4. Launch the Frontend UI
Open `frontend/index.html` directly in Google Chrome, Microsoft Edge, or Mozilla Firefox.

---

## 📑 Project Documentation Links

- 🏛️ [Architecture Documentation](docs/architecture.md)
- ☁️ [AWS Setup & Deployment Guide](docs/aws-setup.md)
- 📡 [REST API Documentation](docs/api-documentation.md)
- 🗄️ [Database Design](docs/database-design.md)
- 🧪 [Testing & Security Checklist](docs/testing.md)
- 🎓 [Complete College Project Report](docs/college-project-report.md)

---

## 🛡️ License
Developed for Academic College Capstone Project Evaluation.
