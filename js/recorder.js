/**
 * Voice Recorder Component using standard MediaRecorder API.
 */
class VoiceRecorder {
  constructor(onStateChange, onTimerUpdate) {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.isRecording = false;
    this.timerInterval = null;
    this.secondsRecorded = 0;
    this.MAX_DURATION_SECONDS = 60; // Auto-stop recording at 60 seconds

    this.onStateChange = onStateChange || (() => {});
    this.onTimerUpdate = onTimerUpdate || (() => {});
  }

  /**
   * Request microphone permission and initialize MediaRecorder
   */
  async startRecording() {
    if (this.isRecording) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      this.audioChunks = [];
      
      // Select best supported MIME type
      let options = {};
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        options = { mimeType: 'audio/webm;codecs=opus' };
      } else if (MediaRecorder.isTypeSupported('audio/webm')) {
        options = { mimeType: 'audio/webm' };
      } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
        options = { mimeType: 'audio/mp4' };
      }

      this.mediaRecorder = new MediaRecorder(stream, options);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.start(250); // Collect data chunks every 250ms
      this.isRecording = true;
      this.secondsRecorded = 0;
      this.startTimer();
      
      this.onStateChange('RECORDING');
    } catch (err) {
      console.error('Microphone access denied or error:', err);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        showToast('Microphone permission was denied. Please allow microphone access in browser settings.', 'error');
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        showToast('No microphone device was detected on your system.', 'error');
      } else {
        showToast('Could not start microphone recording: ' + err.message, 'error');
      }
      this.onStateChange('IDLE');
    }
  }

  /**
   * Stop recording and return Audio Blob
   */
  stopRecording() {
    return new Promise((resolve) => {
      if (!this.mediaRecorder || !this.isRecording) {
        resolve(null);
        return;
      }

      this.stopTimer();

      this.mediaRecorder.onstop = () => {
        const mimeType = this.mediaRecorder.mimeType || 'audio/webm';
        const audioBlob = new Blob(this.audioChunks, { type: mimeType });
        
        // Stop all audio track streams to release hardware mic
        if (this.mediaRecorder.stream) {
          this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }

        this.isRecording = false;
        this.onStateChange('STOPPED');
        resolve(audioBlob);
      };

      this.mediaRecorder.stop();
    });
  }

  startTimer() {
    this.secondsRecorded = 0;
    this.onTimerUpdate(this.secondsRecorded);
    this.timerInterval = setInterval(() => {
      this.secondsRecorded++;
      this.onTimerUpdate(this.secondsRecorded);

      // Auto-stop if recording reaches max limit
      if (this.secondsRecorded >= this.MAX_DURATION_SECONDS) {
        showToast('Maximum recording length (60s) reached', 'info');
        const event = new CustomEvent('voice-max-duration-reached');
        window.dispatchEvent(event);
      }
    }, 1000);
  }

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }
}

