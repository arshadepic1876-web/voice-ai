import os
import logging
from pathlib import Path
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from config.settings import Config

logger = logging.getLogger(__name__)

class S3Service:
    """
    Amazon S3 Storage Service for uploading temporary voice audio recordings.
    Includes graceful local fallback when AWS credentials or buckets are not configured.
    """
    
    def __init__(self):
        self.bucket_name = Config.S3_BUCKET_NAME
        self.region = Config.AWS_REGION
        self.s3_client = None
        
        # Initialize boto3 S3 client if region/bucket are provided
        try:
            self.s3_client = boto3.client('s3', region_name=self.region)
        except Exception as e:
            logger.warning(f"Boto3 S3 client initialization warning: {e}. Running in local fallback mode.")

    def upload_audio(self, local_file_path: Path, object_key: str = None) -> dict:
        """
        Uploads local audio file to S3 bucket under 'recordings/{filename}'.
        
        Returns dict:
        {
            "success": True/False,
            "s3_uri": "s3://bucket-name/recordings/uuid.webm",
            "s3_key": "recordings/uuid.webm",
            "is_local_fallback": True/False
        }
        """
        filename = local_file_path.name
        key = object_key or f"recordings/{filename}"
        
        # If bucket is not set or client fails, use local fallback mode
        if not self.bucket_name or not self.s3_client:
            logger.info("AWS S3 bucket not configured. Using local file storage fallback.")
            return {
                "success": True,
                "s3_uri": f"file://{local_file_path}",
                "s3_key": key,
                "bucket": "local-storage-fallback",
                "is_local_fallback": True
            }
            
        try:
            extra_args = {'ContentType': 'audio/webm'} if filename.endswith('.webm') else {}
            
            logger.info(f"Uploading {local_file_path} to S3 bucket {self.bucket_name} at key {key}...")
            self.s3_client.upload_file(
                Filename=str(local_file_path),
                Bucket=self.bucket_name,
                Key=key,
                ExtraArgs=extra_args
            )
            
            s3_uri = f"s3://{self.bucket_name}/{key}"
            logger.info(f"Successfully uploaded audio to S3: {s3_uri}")
            
            return {
                "success": True,
                "s3_uri": s3_uri,
                "s3_key": key,
                "bucket": self.bucket_name,
                "is_local_fallback": False
            }
        except (BotoCoreError, ClientError) as err:
            logger.error(f"S3 upload failed: {err}. Falling back to local audio handling.")
            return {
                "success": True,
                "s3_uri": f"file://{local_file_path}",
                "s3_key": key,
                "bucket": "local-fallback-after-error",
                "is_local_fallback": True,
                "warning": str(err)
            }

    def delete_audio(self, object_key: str) -> bool:
        """Deletes temporary audio recording from S3 after transcription completes."""
        if not self.bucket_name or not self.s3_client or object_key.startswith("recordings/") is False:
            return True # Nothing to delete in local mode
            
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info(f"Deleted temporary S3 audio file: {object_key}")
            return True
        except Exception as e:
            logger.warning(f"Failed to delete S3 object {object_key}: {e}")
            return False
