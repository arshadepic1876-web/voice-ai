/**
 * Dashboard UI Controller & Event Handlers
 */
document.addEventListener('DOMContentLoaded', async () => {
  console.log('Voice Task Manager Dashboard Initialized');

  // Active Filter state
  let currentFilter = 'all';
  let currentSearchQuery = '';

  // Modal elements
  const modalBackdrop = document.getElementById('preview-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const cancelModalBtn = document.getElementById('cancel-preview-btn');
  const previewForm = document.getElementById('task-preview-form');

  const openModal = () => modalBackdrop.classList.add('open');
  const closeModal = () => modalBackdrop.classList.remove('open');

  if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
  if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);

  // Form Submission -> Save Task to Backend SQLite DB
  if (previewForm) {
    previewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const taskPayload = {
        title: document.getElementById('preview-title').value,
        description: document.getElementById('preview-description').value,
        due_date: document.getElementById('preview-date').value,
        due_time: document.getElementById('preview-time').value,
        priority: document.getElementById('preview-priority').value,
        urgent: document.getElementById('preview-urgency').value === 'true',
        category: document.getElementById('preview-category').value,
        status: 'pending'
      };

      const res = await ApiClient.createTask(taskPayload);
      if (res.success) {
        showToast('Task saved to database successfully!', 'success');
        closeModal();
        loadDashboardTasks();
      } else {
        showToast(res.error || 'Failed to save task', 'error');
      }
    });
  }

  // Load and Render Tasks & Statistics
  async function loadDashboardTasks() {
    const params = {};
    if (currentFilter !== 'all') params.filter = currentFilter;
    if (currentSearchQuery) params.q = currentSearchQuery;

    const res = await ApiClient.getTasks(params);
    const container = document.getElementById('tasks-container');

    if (res.success && res.data) {
      const { tasks, stats } = res.data;

      // Update Dynamic Statistics Counters
      if (stats) {
        document.getElementById('stat-total').innerText = stats.total || 0;
        document.getElementById('stat-pending').innerText = stats.pending || 0;
        document.getElementById('stat-completed').innerText = stats.completed || 0;
        document.getElementById('stat-urgent').innerText = stats.urgent || 0;
        document.getElementById('stat-overdue').innerText = stats.overdue || 0;
      }

      // Render Task Cards
      if (container) {
        if (!tasks || tasks.length === 0) {
          container.innerHTML = TaskManager.renderEmptyState();
        } else {
          container.innerHTML = tasks.map(t => TaskManager.renderTaskCard(t)).join('');
        }
      }
    }
  }

  window.loadTasks = loadDashboardTasks;

  // Search input listener
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentSearchQuery = e.target.value.trim();
      loadDashboardTasks();
    });
  }

  // Filter Buttons Listeners
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const text = btn.innerText.trim().toLowerCase();
      if (text === 'all') currentFilter = 'all';
      else if (text === 'today') currentFilter = 'today';
      else if (text === 'upcoming') currentFilter = 'upcoming';
      else if (text === 'urgent') currentFilter = 'urgent';
      else if (text === 'high priority') currentFilter = 'high_priority';
      else if (text === 'completed') currentFilter = 'completed';

      loadDashboardTasks();
    });
  });

  // Verify backend connectivity on startup
  const health = await ApiClient.checkHealth();
  const statusIndicator = document.getElementById('api-status');
  if (statusIndicator) {
    if (health.success) {
      statusIndicator.innerText = 'Connected';
      statusIndicator.style.color = '#10b981';
      loadDashboardTasks();
    } else {
      statusIndicator.innerText = 'Offline (Start backend app.py)';
      statusIndicator.style.color = '#ef4444';
      showToast('Backend server is offline. Run python backend/app.py', 'error');
    }
  }

  // Initialize Voice Recorder Component
  const micBtn = document.getElementById('mic-btn');
  const recordStatus = document.getElementById('record-status');
  const recordTimer = document.getElementById('record-timer');

  if (micBtn) {
    const recorder = new VoiceRecorder(
      (state) => {
        if (state === 'RECORDING') {
          micBtn.classList.add('recording');
          recordStatus.innerText = 'Listening... Speak your task now';
        } else if (state === 'STOPPED') {
          micBtn.classList.remove('recording');
          recordStatus.innerText = 'Processing audio...';
        } else {
          micBtn.classList.remove('recording');
          recordStatus.innerText = 'Tap microphone to speak';
          recordTimer.innerText = '00:00';
        }
      },
      (seconds) => {
        if (recordTimer) recordTimer.innerText = formatTimer(seconds);
      }
    );

    // Auto-stop listener
    window.addEventListener('voice-max-duration-reached', async () => {
      if (recorder.isRecording) {
        micBtn.click();
      }
    });

    micBtn.addEventListener('click', async () => {
      if (!recorder.isRecording) {
        await recorder.startRecording();
      } else {
        const audioBlob = await recorder.stopRecording();
        if (audioBlob) {
          recordStatus.innerText = 'Transcribing voice & understanding task...';
          const uploadResult = await ApiClient.uploadAudio(audioBlob);
          
          if (uploadResult.success && uploadResult.data) {
            const data = uploadResult.data;
            const task = data.parsed_task || {};
            
            recordStatus.innerText = 'Task detected! Opening preview...';
            showToast('Voice transcribed & task structured successfully!', 'success');
            
            // Populate modal fields
            const transcriptEl = document.getElementById('modal-transcript-text');
            if (transcriptEl) transcriptEl.innerText = `"${data.raw_transcript || 'Speech processed'}"`;

            if (task.title) document.getElementById('preview-title').value = task.title;
            if (task.description) document.getElementById('preview-description').value = task.description;
            if (task.due_date) document.getElementById('preview-date').value = task.due_date;
            if (task.due_time) document.getElementById('preview-time').value = task.due_time;
            if (task.priority) document.getElementById('preview-priority').value = task.priority.toLowerCase();
            
            document.getElementById('preview-urgency').value = task.urgent ? 'true' : 'false';
            if (task.category) document.getElementById('preview-category').value = task.category;
            
            openModal();
            recordStatus.innerText = 'Tap microphone to speak';
          } else {
            recordStatus.innerText = 'Tap microphone to speak';
            showToast(uploadResult.error || 'Audio processing failed', 'error');
          }
        }
      }
    });
  }
});
