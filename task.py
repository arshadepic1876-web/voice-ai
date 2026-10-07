import uuid
from datetime import datetime
import pytz
from config.settings import Config

class Task:
    """
    Task model representing a structured voice-created or manual task.
    """
    
    VALID_PRIORITIES = {'low', 'medium', 'high', 'critical'}
    VALID_CATEGORIES = {'College', 'Study', 'Work', 'Shopping', 'Health', 'Finance', 'Meeting', 'Personal', 'Other'}
    VALID_STATUSES = {'pending', 'in_progress', 'completed'}

    def __init__(
        self,
        title: str,
        description: str = "",
        due_date: str = None,
        due_time: str = None,
        priority: str = "medium",
        urgent: bool = False,
        category: str = "College",
        status: str = "pending",
        raw_transcript: str = "",
        task_id: str = None,
        created_at: str = None,
        updated_at: str = None
    ):
        tz = pytz.timezone(Config.TIMEZONE)
        now_iso = datetime.now(tz).isoformat()
        
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title.strip() if title else "Untitled Task"
        self.description = description.strip() if description else ""
        
        # Default due date to today if missing
        self.due_date = due_date or datetime.now(tz).strftime('%Y-%m-%d')
        self.due_time = due_time or "17:00"
        
        self.priority = priority.lower() if priority and priority.lower() in self.VALID_PRIORITIES else "medium"
        self.urgent = bool(urgent)
        self.category = category.capitalize() if category and category.capitalize() in self.VALID_CATEGORIES else "College"
        self.status = status.lower() if status and status.lower() in self.VALID_STATUSES else "pending"
        
        self.raw_transcript = raw_transcript
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso

    def to_dict(self) -> dict:
        """Serializes Task object to dictionary for JSON API output and DB storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "due_time": self.due_time,
            "priority": self.priority,
            "urgent": self.urgent,
            "category": self.category,
            "status": self.status,
            "raw_transcript": self.raw_transcript,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Instantiates Task object from dictionary payload."""
        if not data:
            return None
            
        return cls(
            task_id=data.get("task_id"),
            title=data.get("title", "Untitled Task"),
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            due_time=data.get("due_time"),
            priority=data.get("priority", "medium"),
            urgent=data.get("urgent", False),
            category=data.get("category", "College"),
            status=data.get("status", "pending"),
            raw_transcript=data.get("raw_transcript", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
