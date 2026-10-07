# Database Architecture & Schema Design
## AI Voice-to-Text Task Manager

---

## 1. SQLite Local Schema

The local development database uses SQLite (`backend/uploads/tasks.db`) encapsulated via `TaskService`.

```sql
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    due_time TEXT,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    urgent INTEGER CHECK(urgent IN (0, 1)),
    category TEXT,
    status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')),
    raw_transcript TEXT,
    created_at TEXT,
    updated_at TEXT
);
```

---

## 2. Amazon DynamoDB Cloud Schema

For persistent production on AWS, the system maps to Amazon DynamoDB.

- **Table Name**: `voice_tasks`
- **Partition Key (`PK`)**: `task_id` (String / UUID)
- **Billing Mode**: PAY_PER_REQUEST (Serverless Free Tier)

```json
{
  "Table": {
    "TableName": "voice_tasks",
    "KeySchema": [
      { "AttributeName": "task_id", "KeyType": "HASH" }
    ],
    "AttributeDefinitions": [
      { "AttributeName": "task_id", "AttributeType": "S" }
    ]
  }
}
```
