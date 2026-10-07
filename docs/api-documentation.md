# REST API Specification & Documentation
## AI Voice-to-Text Task Manager Backend

Base API URL: `http://127.0.0.1:5000/api`

---

## 1. Health Check Endpoint

### `GET /api/health`
Verifies backend server health status, configured timezone, and operational limits.

#### Request Headers:
`Accept: application/json`

#### Response (`200 OK`):
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "AI Voice-to-Text Task Manager Backend",
    "environment": "development",
    "configured_timezone": "Asia/Kolkata",
    "server_time": "2026-10-07T23:25:00+05:30",
    "max_audio_size_mb": 10
  },
  "message": "Voice Task Manager API is running healthy"
}
```

---

## 2. Voice Transcription & Parsing Endpoint

### `POST /api/transcribe`
Receives browser recorded audio blob, validates format/size, uploads to Amazon S3, executes Amazon Transcribe, parses natural speech with NLP engine, and returns structured task draft.

#### Request Headers:
`Content-Type: multipart/form-data`

#### Form Parameters:
- `audio`: Binary audio file (`audio/webm`, `audio/wav`, `audio/mp3`, max 10MB).

#### Response (`200 OK`):
```json
{
  "success": true,
  "data": {
    "recording_id": "c3a8e910-4f81-432d-9831-29e20a9a14bc",
    "raw_transcript": "Remind me to submit my Python assignment tomorrow at 5 PM. It is very important.",
    "parsed_task": {
      "title": "Submit Python assignment",
      "description": "Remind me to submit my Python assignment tomorrow at 5 PM. It is very important.",
      "due_date": "2026-10-08",
      "due_time": "17:00",
      "priority": "high",
      "urgent": false,
      "category": "College",
      "status": "pending"
    }
  },
  "message": "Voice recording transcribed and task attributes parsed successfully"
}
```

---

## 3. Tasks CRUD Endpoints

### `GET /api/tasks`
Retrieves tasks collection with optional query parameters.

#### Query Parameters:
- `filter`: `all` | `today` | `upcoming` | `overdue` | `urgent` | `high_priority` | `completed` | `pending`
- `category`: `College` | `Work` | `Study` | etc.
- `q`: Search term string

#### Response (`200 OK`):
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "task_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "title": "Submit Python assignment",
        "description": "Submit assignment to professor",
        "due_date": "2026-10-08",
        "due_time": "17:00",
        "priority": "high",
        "urgent": true,
        "category": "College",
        "status": "pending",
        "created_at": "2026-10-07T23:20:00+05:30",
        "updated_at": "2026-10-07T23:20:00+05:30"
      }
    ],
    "stats": {
      "total": 1,
      "pending": 1,
      "completed": 0,
      "urgent": 1,
      "overdue": 0
    }
  },
  "message": "Tasks retrieved successfully"
}
```

### `POST /api/tasks`
Creates and persists a structured task.

#### Request Body (`application/json`):
```json
{
  "title": "Submit Python assignment",
  "description": "Submit assignment to professor",
  "due_date": "2026-10-08",
  "due_time": "17:00",
  "priority": "high",
  "urgent": true,
  "category": "College",
  "status": "pending"
}
```

#### Response (`201 Created`):
```json
{
  "success": true,
  "data": {
    "task_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "title": "Submit Python assignment", ...
  },
  "message": "Task created successfully"
}
```

### `PATCH /api/tasks/<task_id>/complete`
Marks task status as completed.

#### Response (`200 OK`):
```json
{
  "success": true,
  "data": {
    "task_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "status": "completed"
  },
  "message": "Task marked as completed"
}
```

### `DELETE /api/tasks/<task_id>`
Deletes task from database.

#### Response (`200 OK`):
```json
{
  "success": true,
  "data": {
    "deleted_task_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  },
  "message": "Task deleted successfully"
}
```
