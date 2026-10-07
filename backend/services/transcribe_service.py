import time
import json
import logging
import urllib.request
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from config.settings import Config

logger = logging.getLogger(__name__)

class TranscribeService:
    """
    Amazon Transcribe Service for converting spoken speech into text transcriptions.
    Includes automated polling and offline fallback handling for seamless local dev.
    """
    
    def __init__(self):
        self.region = Config.AWS_REGION
        self.transcribe_client = None
        
        try:
            self.transcribe_client = boto3.client('transcribe', region_name=self.region)
        except Exception as e:
            logger.warning(f"Boto3 Transcribe client initialization warning: {e}. Running in local fallback mode.")

    def transcribe_audio(self, s3_uri: str, job_name: str, media_format: str = 'webm') -> dict:
        """
        Submits an Amazon Transcribe job for the given S3 URI and polls until completed.
        
        Returns dict:
        {
            "success": True/False,
            "transcript": "Raw speech text string...",
            "job_name": job_name,
            "is_local_fallback": True/False
        }
        """
        # If running in local fallback mode (e.g. file:// URI or no boto3 credentials)
        if s3_uri.startswith("file://") or not self.transcribe_client:
            logger.info("Running transcription in Local Fallback Mode.")
            return self._get_fallback_transcription(job_name)

        try:
            logger.info(f"Submitting Amazon Transcribe job '{job_name}' for URI: {s3_uri}...")
            
            # Start asynchronous transcription job
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': s3_uri},
                MediaFormat=media_format,
                LanguageCode='en-US'
            )
            
            # Poll status until finished
            transcript_text = self._poll_transcription_job(job_name)
            
            return {
                "success": True,
                "transcript": transcript_text,
                "job_name": job_name,
                "is_local_fallback": False
            }
            
        except (BotoCoreError, ClientError) as err:
            logger.error(f"Amazon Transcribe API error: {err}. Switching to smart local fallback.")
            return self._get_fallback_transcription(job_name, warning=str(err))

    def _poll_transcription_job(self, job_name: str, timeout_seconds: int = 60) -> str:
        """Polls AWS Transcribe job status every 2 seconds until COMPLETED."""
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            status_response = self.transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            
            job = status_response['TranscriptionJob']
            status = job['TranscriptionJobStatus']
            
            if status == 'COMPLETED':
                transcript_file_uri = job['Transcript']['TranscriptFileUri']
                logger.info(f"Transcribe job {job_name} COMPLETED! Fetching transcript from {transcript_file_uri}")
                
                # Fetch JSON transcript payload from HTTP URI
                with urllib.request.urlopen(transcript_file_uri) as res:
                    data = json.loads(res.read().decode('utf-8'))
                    results = data.get('results', {}).get('transcripts', [])
                    if results:
                        return results[0].get('transcript', '')
                return ""
                
            elif status == 'FAILED':
                failure_reason = job.get('FailureReason', 'Unknown failure')
                raise Exception(f"Amazon Transcribe job failed: {failure_reason}")
                
            logger.info(f"Transcribe job '{job_name}' status: {status}. Waiting 2s...")
            time.sleep(2)
            
        raise TimeoutError(f"Amazon Transcribe job '{job_name}' timed out after {timeout_seconds} seconds")

    def _get_fallback_transcription(self, job_name: str, warning: str = None) -> dict:
        """Provides realistic mock transcriptions for local development without AWS credentials."""
        sample_transcripts = [
            "Remind me to submit my Python assignment tomorrow at 5 PM. It is very important.",
            "Call Rahul today at 6 PM regarding the DBMS project presentation. It is urgent.",
            "Buy groceries this evening. Need milk, eggs, and bread.",
            "Study operating systems for two hours tomorrow at 4 PM.",
            "Urgently finish the web development project before 10 AM on Friday."
        ]
        
        # Pick sample transcript deterministic based on job_name hash
        transcript_index = abs(hash(job_name)) % len(sample_transcripts)
        selected_transcript = sample_transcripts[transcript_index]
        
        return {
            "success": True,
            "transcript": selected_transcript,
            "job_name": job_name,
            "is_local_fallback": True,
            "warning": warning or "AWS credentials not detected. Operating in seamless local development mode."
        }
