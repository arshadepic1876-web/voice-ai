import re
from datetime import datetime, timedelta
import pytz
from dateutil import parser as date_parser
from config.settings import Config

class TaskParser:
    """
    Intelligent NLP Task Parser.
    Extracts structured task metadata (title, due_date, due_time, priority, urgency, category)
    from natural speech transcriptions.
    """
    
    @classmethod
    def parse_transcript(cls, transcript: str) -> dict:
        """
        Parses raw transcript string into structured task JSON dictionary.
        """
        if not transcript:
            return cls._get_empty_task_schema("")
            
        clean_text = transcript.strip()
        lower_text = clean_text.lower()
        
        # 1. Resolve Timezone & Base Date
        tz = pytz.timezone(Config.TIMEZONE)
        now = datetime.now(tz)
        
        # 2. Extract Urgency Flag
        is_urgent = cls._extract_urgency(lower_text)
        
        # 3. Extract Priority Level
        priority = cls._extract_priority(lower_text)
        
        # 4. Extract Category
        category = cls._extract_category(lower_text)
        
        # 5. Extract Date & Time
        due_date, due_time = cls._extract_date_and_time(lower_text, now)
        
        # 6. Extract Clean Title & Description
        title = cls._extract_title(clean_text, lower_text)
        
        return {
            "title": title,
            "description": clean_text,
            "due_date": due_date,
            "due_time": due_time,
            "priority": priority,
            "urgent": is_urgent,
            "category": category,
            "status": "pending",
            "raw_transcript": clean_text,
            "parsed_at": now.isoformat()
        }

    @classmethod
    def _extract_urgency(cls, text: str) -> bool:
        urgent_keywords = ['urgent', 'urgently', 'asap', 'immediately', 'right now', 'emergency']
        return any(keyword in text for keyword in urgent_keywords)

    @classmethod
    def _extract_priority(cls, text: str) -> str:
        if any(k in text for k in ['critical', 'highest priority', 'crucial']):
            return 'critical'
        elif any(k in text for k in ['very important', 'important', 'high priority', 'must do']):
            return 'high'
        elif any(k in text for k in ['not important', 'low priority', 'whenever', 'optional']):
            return 'low'
        return 'medium'

    @classmethod
    def _extract_category(cls, text: str) -> str:
        categories = {
            'College': ['assignment', 'professor', 'lab', 'viva', 'college', 'homework', 'submission', 'campus'],
            'Study': ['study', 'read', 'operating systems', 'dbms', 'algorithms', 'python', 'exam', 'revision'],
            'Work': ['meeting', 'presentation', 'client', 'office', 'boss', 'report', 'deadline'],
            'Shopping': ['buy', 'groceries', 'milk', 'eggs', 'bread', 'store', 'market', 'purchase'],
            'Health': ['doctor', 'medicine', 'workout', 'gym', 'hospital', 'clinic', 'pills'],
            'Finance': ['pay', 'bill', 'rent', 'fees', 'bank', 'transfer', 'recharge'],
            'Meeting': ['call', 'meet', 'zoom', 'teams', 'discussion']
        }
        
        for category, keywords in categories.items():
            if any(k in text for k in keywords):
                return category
                
        return 'Personal'

    @classmethod
    def _extract_date_and_time(cls, text: str, now: datetime) -> tuple:
        target_date = now.date()
        target_time_str = "17:00" # Default 5:00 PM if unspecified
        
        # Date extraction logic
        if 'tomorrow' in text:
            target_date = (now + timedelta(days=1)).date()
        elif 'today' in text or 'tonight' in text or 'this evening' in text:
            target_date = now.date()
        elif 'next monday' in text:
            days_ahead = 7 - now.weekday()
            target_date = (now + timedelta(days=days_ahead)).date()
        elif 'friday' in text:
            days_ahead = (4 - now.weekday()) % 7
            if days_ahead == 0: days_ahead = 7
            target_date = (now + timedelta(days=days_ahead)).date()

        # Time extraction using Regex (e.g., "5 PM", "10:30 AM", "4 PM")
        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            meridiem = time_match.group(3).lower()
            
            if meridiem == 'pm' and hour < 12:
                hour += 12
            elif meridiem == 'am' and hour == 12:
                hour = 0
                
            target_time_str = f"{hour:02d}:{minute:02d}"
            
        return target_date.strftime('%Y-%m-%d'), target_time_str

    @classmethod
    def _extract_title(cls, clean_text: str, lower_text: str) -> str:
        """Removes noise words like 'Remind me to' or 'Urgently' to extract a concise task title."""
        title = clean_text
        
        # Strip common action prefixes
        patterns = [
            r'^(remind me to\s+)',
            r'^(i need to\s+)',
            r'^(please\s+)',
            r'^(urgently\s+)',
            r'^(remember to\s+)'
        ]
        
        for pattern in patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
            
        # Capitalize title
        return title[0].upper() + title[1:] if title else "New Voice Task"

    @classmethod
    def _get_empty_task_schema(cls, transcript: str) -> dict:
        return {
            "title": "New Voice Task",
            "description": transcript,
            "due_date": datetime.now().strftime('%Y-%m-%d'),
            "due_time": "17:00",
            "priority": "medium",
            "urgent": False,
            "category": "Personal",
            "status": "pending",
            "raw_transcript": transcript
        }
