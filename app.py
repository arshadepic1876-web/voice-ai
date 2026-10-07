import sys
from pathlib import Path

# Add backend directory to Python sys.path for clean relative imports
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from flask import Flask
from flask_cors import CORS
from config.settings import Config
from utils.errors import register_error_handlers
from routes.health import health_bp
from routes.transcription import transcription_bp
from routes.tasks import tasks_bp

def create_app():
    """Flask Application Factory."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    Config.ensure_directories()
    
    # Enable CORS for all routes (allows frontend browser requests)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints (routes)
    app.register_blueprint(health_bp)
    app.register_blueprint(transcription_bp)
    app.register_blueprint(tasks_bp)
    
    # Register global error handlers
    register_error_handlers(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    print(f"🚀 Starting AI Voice Task Manager Backend on http://127.0.0.1:{Config.PORT}")
    print(f"🌍 Configured Timezone: {Config.TIMEZONE}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
