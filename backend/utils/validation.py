import os
from werkzeug.datastructures import FileStorage

ALLOWED_EXTENSIONS = {'webm', 'wav', 'mp3', 'm4a', 'ogg'}
ALLOWED_MIME_TYPES = {
    'audio/webm',
    'audio/wav',
    'audio/x-wav',
    'audio/mp3',
    'audio/mpeg',
    'audio/ogg',
    'audio/mp4',
    'audio/x-m4a'
}

def validate_audio_file(file: FileStorage, max_size_mb: int = 10):
    """
    Validates uploaded audio file against format, size, and content constraints.
    Returns (is_valid: bool, error_message: str)
    """
    if not file or not file.filename:
        return False, "No audio file provided in request"
    
    filename = file.filename
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported audio file format '.{ext}'. Supported formats: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check MIME type if provided by browser
    if file.mimetype and file.mimetype not in ALLOWED_MIME_TYPES:
        # Browser webm recordings often come as audio/webm;codecs=opus
        base_mime = file.mimetype.split(';')[0].strip()
        if base_mime not in ALLOWED_MIME_TYPES:
            return False, f"Invalid audio MIME type: {file.mimetype}"
            
    # Check file size by seeking
    file.seek(0, os.SEEK_END)
    size_bytes = file.tell()
    file.seek(0)  # Reset pointer for subsequent reading
    
    if size_bytes == 0:
        return False, "Audio recording is empty (0 bytes)"
        
    max_bytes = max_size_mb * 1024 * 1024
    if size_bytes > max_bytes:
        return False, f"Audio file size ({round(size_bytes / (1024*1024), 2)}MB) exceeds maximum allowed limit of {max_size_mb}MB"
        
    return True, ""
