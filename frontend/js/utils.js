/**
 * Utility functions for UI formatting, notifications, and dates.
 */

// Toast notification display
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerText = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Seconds to MM:SS formatting
function formatTimer(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Priority badge HTML builder
function getPriorityBadgeHTML(priority) {
  const p = (priority || 'medium').toLowerCase();
  return `<span class="badge badge-${p}">${p}</span>`;
}

// Urgency badge HTML builder
function getUrgencyBadgeHTML(isUrgent) {
  if (!isUrgent) return '';
  return `<span class="badge badge-urgent">⚡ Urgent</span>`;
}

// Escape HTML for XSS safety
function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}
