from flask import Blueprint
from utils.errors import api_response
from config.settings import Config
from datetime import datetime
import pytz

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health', methods=['GET'])
def check_health():
    """
    Health check endpoint to verify backend service state, timezone, and environment config.
    """
    tz = pytz.timezone(Config.TIMEZONE)
    current_time = datetime.now(tz).isoformat()
    
    health_data = {
        "status": "healthy",
        "service": "AI Voice-to-Text Task Manager Backend",
        "environment": Config.ENV,
        "configured_timezone": Config.TIMEZONE,
        "server_time": current_time,
        "max_audio_size_mb": Config.MAX_AUDIO_SIZE_MB
    }
    
    return api_response(
        success=True,
        data=health_data,
        message="Voice Task Manager API is running healthy",
        status_code=200
    )
