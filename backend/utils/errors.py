from flask import jsonify

def api_response(success: bool, data=None, message: str = "", status_code: int = 200):
    """
    Standardized REST API JSON response structure.
    
    Example Success Output:
    {
        "success": true,
        "data": { ... },
        "message": "Task created successfully"
    }
    """
    payload = {
        "success": success,
        "data": data,
        "message": message
    }
    return jsonify(payload), status_code

def error_response(message: str, status_code: int = 400, details=None):
    """Standardized error response formatter."""
    payload = {
        "success": False,
        "error": message,
        "details": details or {}
    }
    return jsonify(payload), status_code

def register_error_handlers(app):
    """Registers global exception handlers for the Flask app."""
    
    @app.errorhandler(400)
    def bad_request(e):
        return error_response(str(e.description) if hasattr(e, 'description') else "Bad request", 400)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Requested endpoint or resource was not found", 404)

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return error_response("Uploaded audio exceeds the maximum allowed size limit (10MB)", 413)

    @app.errorhandler(500)
    def internal_server_error(e):
        return error_response("An internal server error occurred. Please try again later.", 500)
