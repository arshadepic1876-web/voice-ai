import os
from pathlib import Path
from dotenv import load_dotenv

# Base backend directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Central configuration class for Flask application settings."""
    
    # Flask settings
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = (ENV == 'development')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key')
    
    # Application settings
    TIMEZONE = os.getenv('TIMEZONE', 'Asia/Kolkata')
    MAX_AUDIO_SIZE_MB = int(os.getenv('MAX_AUDIO_SIZE_MB', 10))
    MAX_CONTENT_LENGTH = MAX_AUDIO_SIZE_MB * 1024 * 1024  # In Bytes for Flask
    
    # Upload path
    UPLOAD_FOLDER = BASE_DIR / os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # AWS settings
    AWS_REGION = os.getenv('AWS_REGION', 'ap-south-1')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', '')

    @classmethod
    def ensure_directories(cls):
        """Ensure required local directories (like uploads) exist."""
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
