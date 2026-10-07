# AWS Cloud Setup & EC2 Deployment Guide
## AI Voice-to-Text Task Manager

---

## 1. Prerequisites & AWS Account Setup
- An active AWS Account.
- Recommended AWS Region: `ap-south-1` (Mumbai) or `us-east-1` (N. Virginia).

---

## 2. Amazon S3 Configuration

1. Open **Amazon S3 Console** ──► Click **Create Bucket**.
2. **Bucket Name**: `voice-task-manager-audio-bucket-<your-name>` (Must be globally unique).
3. **Region**: `ap-south-1`.
4. **Block Public Access**: Keep **Block ALL public access** ENABLED (Private bucket security).
5. Click **Create Bucket**.

### Lifecycle Rules (Automatic Audio Cleanup):
1. Select your bucket ──► **Management** tab ──► **Create lifecycle rule**.
2. **Rule Name**: `AutoDeleteTempRecordings`.
3. **Prefix filter**: `recordings/`.
4. **Expiration action**: Expire current versions after **1 day**.

---

## 3. AWS IAM Policy & EC2 Role Setup

Create an IAM Role with least-privilege permissions to attach to the EC2 instance:

1. Open **IAM Console** ──► **Roles** ──► **Create Role**.
2. **Trusted Entity**: AWS Service ──► **EC2**.
3. Attach Policies:
   - `AmazonTranscribeFullAccess`
   - Custom S3 Policy (or `AmazonS3FullAccess` for bucket `voice-task-manager-audio-bucket`)

---

## 4. Amazon EC2 Deployment Guide

### A. Launch Instance
1. Open **EC2 Console** ──► **Launch Instance**.
2. **Name**: `VoiceTask-AI-Server`.
3. **AMI**: Ubuntu Server 22.04 LTS (64-bit).
4. **Instance Type**: `t2.micro` or `t3.micro` (Free Tier Eligible).
5. **Key Pair**: Select existing key pair or create a new `.pem` key.
6. **Network / Security Group**:
   - Allow **SSH (Port 22)** from your IP.
   - Allow **HTTP (Port 80)** from Anywhere (`0.0.0.0/0`).
   - Allow **Custom TCP (Port 5000)** from Anywhere (For testing API).
7. Attach the IAM Role created in Section 3 to this instance.

### B. Connect and Install Environment
SSH into EC2 instance:

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

Update packages & install Python, Nginx:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```

### C. Upload Project & Install Backend

```bash
git clone <your-repo-url> VoiceAi
cd VoiceAi/backend

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### D. Configure Production Environment Variables
Create `.env`:

```env
FLASK_ENV=production
FLASK_PORT=5000
SECRET_KEY=production-super-secret-key-998877
TIMEZONE=Asia/Kolkata
AWS_REGION=ap-south-1
S3_BUCKET_NAME=voice-task-manager-audio-bucket-your-name
MAX_AUDIO_SIZE_MB=10
UPLOAD_FOLDER=uploads
```

### E. Run Production Gunicorn Server

```bash
gunicorn --bind 0.0.0.0:5000 app:app --workers 3 --daemon
```

### F. Configure Nginx Reverse Proxy
Edit `/etc/nginx/sites-available/default`:

```nginx
server {
    listen 80;
    server_name _;

    location / {
        root /home/ubuntu/VoiceAi/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

Now open your EC2 Public IP in browser: `http://<your-ec2-public-ip>` 🚀

---

## 5. Cost Control & Cleanup Checklist

- [x] Delete temporary S3 recordings immediately after transcription.
- [x] Configure 1-day S3 Lifecycle Expiration policy.
- [x] Terminate or stop EC2 instance when evaluation is finished.
- [x] Delete S3 bucket resources after final presentation.
