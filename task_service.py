import sqlite3
import logging
from pathlib import Path
from datetime import datetime
import pytz
from config.settings import Config
from models.task import Task

logger = logging.getLogger(__name__)

class TaskService:
    """
    Task Persistence & Repository Service using SQLite.
    Provides complete CRUD operations, query filters, search, and dynamic stats.
    Easily swappable with DynamoDB for cloud deployment.
    """
    
    DB_PATH = Config.UPLOAD_FOLDER / 'tasks.db'

    @classmethod
    def _get_connection(cls):
        """Creates and returns SQLite connection with row factory enabled."""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(cls.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls):
        """Initializes tasks SQL schema table if it does not exist."""
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    due_time TEXT,
                    priority TEXT,
                    urgent INTEGER,
                    category TEXT,
                    status TEXT,
                    raw_transcript TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            conn.commit()
            logger.info("SQLite task database initialized successfully.")

    @classmethod
    def create_task(cls, task_data: dict) -> dict:
        """Creates and persists a new task in SQLite DB."""
        cls.init_db()
        task = Task.from_dict(task_data)
        d = task.to_dict()
        
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (
                    task_id, title, description, due_date, due_time,
                    priority, urgent, category, status, raw_transcript,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                d['task_id'], d['title'], d['description'], d['due_date'], d['due_time'],
                d['priority'], 1 if d['urgent'] else 0, d['category'], d['status'],
                d['raw_transcript'], d['created_at'], d['updated_at']
            ))
            conn.commit()
            
        logger.info(f"Created task: {d['title']} (ID: {d['task_id']})")
        return d

    @classmethod
    def get_all_tasks(cls, filter_by: str = None, category: str = None, search_query: str = None) -> dict:
        """
        Retrieves all tasks with optional filters, search, and dynamic summary statistics.
        """
        cls.init_db()
        tz = pytz.timezone(Config.TIMEZONE)
        today_str = datetime.now(tz).strftime('%Y-%m-%d')
        
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if category and category != 'All':
            query += " AND category = ?"
            params.append(category)

        if search_query:
            query += " AND (title LIKE ? OR description LIKE ? OR category LIKE ?)"
            term = f"%{search_query}%"
            params.extend([term, term, term])

        # Apply Quick Filters
        if filter_by == 'today':
            query += " AND due_date = ?"
            params.append(today_str)
        elif filter_by == 'upcoming':
            query += " AND due_date > ? AND status != 'completed'"
            params.append(today_str)
        elif filter_by == 'overdue':
            query += " AND due_date < ? AND status != 'completed'"
            params.append(today_str)
        elif filter_by == 'urgent':
            query += " AND urgent = 1"
        elif filter_by == 'high_priority':
            query += " AND (priority = 'high' OR priority = 'critical')"
        elif filter_by == 'completed':
            query += " AND status = 'completed'"
        elif filter_by == 'pending':
            query += " AND status != 'completed'"

        # Sort: Urgent -> Overdue -> Due soon -> Created
        query += " ORDER BY urgent DESC, due_date ASC, due_time ASC, created_at DESC"

        tasks_list = []
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, params).fetchall()
            for r in rows:
                tasks_list.append(cls._row_to_dict(r))

            # Compute Summary Statistics
            all_rows = cursor.execute("SELECT due_date, status, urgent FROM tasks").fetchall()
            
            stats = {
                "total": len(all_rows),
                "pending": 0,
                "completed": 0,
                "urgent": 0,
                "overdue": 0
            }
            
            for row in all_rows:
                status = row['status']
                due_date = row['due_date']
                is_urg = row['urgent']
                
                if status == 'completed':
                    stats['completed'] += 1
                else:
                    stats['pending'] += 1
                    if due_date and due_date < today_str:
                        stats['overdue'] += 1
                        
                if is_urg:
                    stats['urgent'] += 1

        return {
            "tasks": tasks_list,
            "stats": stats
        }

    @classmethod
    def get_task_by_id(cls, task_id: str) -> dict:
        """Retrieves a single task by ID."""
        cls.init_db()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
            if row:
                return cls._row_to_dict(row)
        return None

    @classmethod
    def update_task(cls, task_id: str, update_data: dict) -> dict:
        """Updates attributes of an existing task."""
        cls.init_db()
        existing = cls.get_task_by_id(task_id)
        if not existing:
            return None

        # Merge update fields
        existing.update(update_data)
        tz = pytz.timezone(Config.TIMEZONE)
        existing['updated_at'] = datetime.now(tz).isoformat()

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks SET
                    title = ?, description = ?, due_date = ?, due_time = ?,
                    priority = ?, urgent = ?, category = ?, status = ?, updated_at = ?
                WHERE task_id = ?
            ''', (
                existing['title'], existing['description'], existing['due_date'], existing['due_time'],
                existing['priority'], 1 if existing['urgent'] else 0, existing['category'],
                existing['status'], existing['updated_at'], task_id
            ))
            conn.commit()

        return existing

    @classmethod
    def complete_task(cls, task_id: str) -> dict:
        """Marks a task status as completed."""
        return cls.update_task(task_id, {"status": "completed"})

    @classmethod
    def delete_task(cls, task_id: str) -> bool:
        """Deletes a task from SQLite DB."""
        cls.init_db()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    @classmethod
    def _row_to_dict(cls, row) -> dict:
        d = dict(row)
        d['urgent'] = bool(d['urgent'])
        return d
