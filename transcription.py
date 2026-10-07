import uuid
import logging
from pathlib import Path
from flask import Blueprint, request
from utils.errors import api_response, error_response
from utils.validation import validate_audio_file
from config.settings import Config
from services.s3_service import S3Service
from services.transcribe_service import TranscribeService
from services.task_parser import TaskParser

logger = logging.getLogger(__name__)

transcription_bp = Blueprint('transcription', __name__)

s3_service = S3Service()
transcribe_service = TranscribeService()

@transcription_bp.route('/api/transcribe', methods=['POST'])
def handle_transcription():
    """
    POST /api/transcribe
    Complete Pipeline:
    1. Validates incoming browser audio recording blob.
    2. Saves locally with UUID key.
    3. Uploads audio file to Amazon S3.
    4. Triggers Amazon Transcribe job & polls for completed speech-to-text transcript.
    5. Runs AI Task Parser to extract structured task attributes (title, due_date, due_time, priority, urgency, category).
    6. Returns structured preview payload for user confirmation.
    """
    if 'audio' not in request.files:
        return error_response("No audio file provided in request", status_code=400)
        
    audio_file = request.files['audio']
    is_valid, err_msg = validate_audio_file(audio_file, max_size_mb=Config.MAX_AUDIO_SIZE_MB)
    
    if not is_valid:
        return error_response(err_msg, status_code=400)
        
    # Step 1: Save recording locally
    ext = audio_file.filename.rsplit('.', 1)[-1].lower() if '.' in audio_file.filename else 'webm'
    recording_id = str(uuid.uuid4())
    saved_filename = f"recording_{recording_id}.{ext}"
    saved_path = Config.UPLOAD_FOLDER / saved_filename
    
    try:
        audio_file.save(saved_path)
    except Exception as e:
        return error_response(f"Failed to save audio recording on server: {str(e)}", status_code=500)
        
    # Step 2: Upload audio recording to Amazon S3
    s3_key = f"recordings/{saved_filename}"
    s3_result = s3_service.upload_audio(saved_path, object_key=s3_key)
    
    # Step 3: Trigger Amazon Transcribe job
    job_name = f"transcribe_job_{recording_id[:8]}"
    transcribe_result = transcribe_service.transcribe_audio(
        s3_uri=s3_result['s3_uri'],
        job_name=job_name,
        media_format=ext if ext in ['webm', 'wav', 'mp3'] else 'webm'
    )
    
    raw_transcript = transcribe_result.get('transcript', '')
    
    # Step 4: Run AI NLP Task Parser
    parsed_task = TaskParser.parse_transcript(raw_transcript)
    
    # Step 5: Clean up temporary S3 object after transcription
    s3_service.delete_audio(s3_key)
    
    return api_response(
        success=True,
        data={
            "recording_id": recording_id,
            "raw_transcript": raw_transcript,
            "parsed_task": parsed_task,
            "s3_info": {
                "bucket": s3_result.get('bucket'),
                "is_fallback": s3_result.get('is_local_fallback', False)
            },
            "transcribe_info": {
                "job_name": job_name,
                "is_fallback": transcribe_result.get('is_local_fallback', False)
            }
        },
        message="Voice recording transcribed and task attributes parsed successfully",
        status_code=200
    )


