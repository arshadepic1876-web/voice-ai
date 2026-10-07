# College Project Report
# AI Voice-to-Text Task Manager using AWS

---

## 1. Project Title
**AI Voice-to-Text Task Manager using AWS Cloud Infrastructure**

---

## 2. Abstract
Modern productivity tools often require users to manually navigate multiple input fields, select dropdown menus, pick calendars, and configure priority flags to create structured tasks. This project presents **AI Voice-to-Text Task Manager**, an intelligent, cloud-native web application that automates task creation through natural voice speech. The system captures microphone audio in the browser, securely uploads temporary recordings to **Amazon S3**, transcribes speech into text using **Amazon Transcribe**, processes natural language with an **AI Task Parser Engine**, and extracts structured task attributes (Title, Date, Time, Priority, Urgency, Category). Built with a decoupled **HTML5/Vanilla JS** frontend and **Python/Flask** REST API backend, the system is fully deployable on **Amazon EC2** with **Amazon DynamoDB/SQLite** database persistence.

---

## 3. Introduction
In today's fast-paced academic and professional environments, efficient task management is essential. However, traditional task management applications suffer from input friction—forcing users to type titles, pick dates, set timers, and assign categories manually. Voice user interfaces (VUIs) coupled with cloud speech recognition and natural language understanding offer a transformative alternative. This application enables users to speak naturally (e.g. *"Remind me to submit my Python assignment tomorrow at 5 PM. It is very important."*) and automatically structures the task without manual form entry.

---

## 4. Problem Statement
Conventional task management interfaces require manual keyboard and mouse interactions across multiple form fields. This manual process causes several problems:
1. **High Input Friction**: Creating a task takes 30–60 seconds of manual typing and date picker navigation.
2. **Context Switching**: Interrupts flow state during lectures, meetings, or mobile movement.
3. **Lack of Natural Language Intelligence**: Traditional apps do not understand relative phrases like *"tomorrow at 5 PM"* or *"urgently finish by Friday"*.

---

## 5. Existing System
Existing task managers (e.g., standard todo apps) rely heavily on manual text forms:
- **Disadvantages**:
  - Requires physical typing and manual selection of date pickers.
  - Does not parse natural language relative dates or implicit priorities.
  - Requires strong internet connections with heavy client framework overhead.

---

## 6. Proposed System
The proposed system introduces an AI-powered voice task management application:
- **Speech Recognition**: Uses Amazon Transcribe for high-accuracy speech-to-text.
- **Natural Language Parsing**: Automatically extracts Title, Date, Time, Priority level (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), Urgency flag (`URGENT`/`NORMAL`), and Category (`College`, `Work`, `Study`, `Shopping`, `Health`, `Finance`, `Meeting`, `Personal`).
- **Interactive Preview & Confirmation**: Displays a preview modal allowing the user to review or edit extracted attributes before saving.
- **Cloud-Native AWS Deployment**: Hosted on Amazon EC2 with S3 audio storage and IAM least-privilege security.

---

## 7. Objectives
1. Build a production-grade web application with complete frontend/backend separation.
2. Integrate browser microphone recording using standard `MediaRecorder API`.
3. Connect Amazon S3 and Amazon Transcribe via `boto3` SDK.
4. Develop an NLP Task Parser that resolves relative dates against `Asia/Kolkata` timezone.
5. Create a dynamic, responsive cosmic glassmorphism dashboard.
6. Provide full CRUD REST API endpoints and database persistence.

---

## 8. Technologies Used

- **Frontend**: HTML5, CSS3 (Vanilla CSS Glassmorphism), Vanilla JavaScript (ES6+), Fetch API, MediaRecorder API.
- **Backend**: Python 3.11, Flask framework, Flask-CORS, `boto3`, `python-dotenv`, `python-dateutil`, `pytz`.
- **AWS Cloud**: Amazon S3, Amazon Transcribe, Amazon EC2, AWS IAM.
- **Database**: SQLite (Development) / Amazon DynamoDB (Production).
- **Web Server**: Gunicorn, Nginx reverse proxy.

---

## 9. System Requirements

### Hardware Requirements:
- Processor: Dual-Core 2.0 GHz or higher.
- RAM: 4 GB minimum.
- Storage: 10 GB available disk space.
- Input Device: System Microphone for audio capture.

### Software Requirements:
- OS: Windows 10/11, macOS, or Ubuntu 22.04 LTS.
- Browser: Google Chrome, Microsoft Edge, or Mozilla Firefox.
- Python: Version 3.10 or higher.
- AWS Account: Active account with IAM privileges.

---

## 10. Functional Requirements
- **FR1**: User can record audio up to 60 seconds directly in the browser.
- **FR2**: System validates audio size (<10MB) and MIME format (`audio/webm`, `audio/wav`).
- **FR3**: System uploads audio to S3 and triggers Amazon Transcribe speech recognition.
- **FR4**: System parses transcript to extract Title, Date, Time, Priority, Urgency, and Category.
- **FR5**: System shows a Task Preview Confirmation Modal before saving.
- **FR6**: System supports creating, reading, completing, editing, and deleting tasks.
- **FR7**: System provides real-time search, quick filters, and dynamic stats counters.

---

## 11. Non-functional Requirements
- **NFR1 Performance**: Voice transcription and parsing completes within <5 seconds.
- **NFR2 Security**: Zero AWS credentials in frontend; IAM roles used for EC2 authorization.
- **NFR3 Usability**: Modern cosmic glassmorphism UI with responsive support for mobile, tablet, and desktop.
- **NFR4 Reliability**: Includes graceful local fallback mode for offline testing.

---

## 12. System Architecture
The application uses a two-tier decoupled architecture:
1. **Frontend Tier**: Pure HTML5/CSS3/JS client communicating over HTTPS/REST.
2. **Backend Tier**: Flask server handling validation, S3 uploads, Transcribe jobs, NLP parsing, and DB persistence.

---

## 13. Data Flow
`User Speech` ──► `MediaRecorder API` ──► `Flask API` ──► `Amazon S3` ──► `Amazon Transcribe` ──► `NLP Parser` ──► `Task Preview Modal` ──► `Database`

---

## 14. Sequence Diagram
*(Refer to `docs/architecture.md` for full sequence diagram)*

---

## 15. Modules
1. **Voice Recording Module** (`frontend/js/recorder.js`)
2. **Audio Upload & Validation Module** (`backend/utils/validation.py`)
3. **Amazon S3 Storage Service** (`backend/services/s3_service.py`)
4. **Amazon Transcribe Speech Service** (`backend/services/transcribe_service.py`)
5. **AI Task Parser Engine** (`backend/services/task_parser.py`)
6. **Task Repository & DB Persistence Service** (`backend/services/task_service.py`)
7. **REST API Controller Routes** (`backend/routes/*`)
8. **Cosmic Dashboard UI Module** (`frontend/js/dashboard.js`)

---

## 16. Working Methodology
1. **Recording**: User clicks the glowing microphone orb in browser.
2. **Upload**: Audio Blob sent via HTTP POST to `/api/transcribe`.
3. **Cloud Processing**: S3 stores audio; Transcribe executes ASR.
4. **Information Extraction**: `TaskParser` extracts attributes and formats times/dates.
5. **Confirmation**: Preview modal pops up with filled fields for user validation.
6. **Persistence**: Saved task is inserted into SQLite/DynamoDB and rendered on dashboard.

---

## 17. AWS Architecture
- **S3 Bucket**: Private object store with 1-day lifecycle expiration.
- **Transcribe**: Asynchronous ASR batch processing.
- **EC2 Instance**: `t2.micro` Ubuntu server running Gunicorn + Nginx.
- **IAM Role**: Attached to EC2 with least-privilege policies.

---

## 18. Database Design
*(Refer to `docs/database-design.md` for SQLite & DynamoDB schemas)*

---

## 19. API Design
*(Refer to `docs/api-documentation.md` for complete REST endpoints reference)*

---

## 20. Implementation
All source code is organized modularly under `frontend/` and `backend/`. Standard practices including `.env` environment isolation, CORS security, input sanitization, and structured JSON responses are implemented.

---

## 21. Testing
*(Refer to `docs/testing.md` for 25-case testing verification matrix)*

---

## 22. Advantages
1. **Zero Typing Needed**: Tasks created in seconds via voice.
2. **Natural Language Understanding**: Resolves relative dates like *"tomorrow at 5 PM"*.
3. **Cloud Native**: Scalable AWS infrastructure.
4. **Cost Efficient**: Automatic S3 file deletion after transcription.

---

## 23. Limitations
1. Speech recognition accuracy depends on microphone audio quality and background noise.
2. Requires browser microphone permission access.

---

## 24. Future Scope
1. **Streaming Speech Recognition**: Real-time live transcript typing using AWS Transcribe Streaming WebSockets.
2. **Multi-User Authentication**: User login and privacy using Amazon Cognito.
3. **Push Notifications**: Task reminders via Amazon SNS / SES.

---

## 25. Conclusion
The **AI Voice-to-Text Task Manager** successfully demonstrates the integration of cloud speech recognition, artificial intelligence, natural language parsing, and modern full-stack web development. The application provides an intuitive voice-first user experience while maintaining robust enterprise security and cost-efficient cloud architecture.

---

## 26. References
1. Amazon Web Services Documentation — Amazon Transcribe & S3 Developer Guides.
2. Flask Web Development Documentation (Pallets Projects).
3. MDN Web Docs — MediaRecorder API & Fetch API Specification.
4. Python boto3 SDK Documentation.
