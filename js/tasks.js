/**
 * Tasks View Controller (Search, Filter, Render, CRUD)
 */
class TaskManager {
  /**
   * Render single task card HTML string
   */
  static renderTaskCard(task) {
    const isUrgent = task.urgent || false;
    const isCompleted = task.status === 'completed';
    const priorityBadge = getPriorityBadgeHTML(task.priority);
    const urgentBadge = getUrgencyBadgeHTML(isUrgent);
    const taskId = task.task_id || task.id;

    return `
      <div class="task-card ${isUrgent ? 'urgent' : ''} ${isCompleted ? 'completed' : ''}" id="task-card-${taskId}" data-id="${taskId}">
        <div class="task-header">
          <h3 class="task-title" style="${isCompleted ? 'text-decoration: line-through; opacity: 0.6;' : ''}">
            ${escapeHTML(task.title)}
          </h3>
          <div>${priorityBadge} ${urgentBadge}</div>
        </div>
        
        ${task.description ? `<p class="task-description" style="margin-bottom:0.75rem; color:var(--text-muted); font-size:0.9rem;">${escapeHTML(task.description)}</p>` : ''}
        
        <div class="task-meta">
          <span>📅 ${escapeHTML(task.due_date || 'No date')}</span>
          <span>⏰ ${escapeHTML(task.due_time || 'No time')}</span>
          <span>📚 ${escapeHTML(task.category || 'College')}</span>
        </div>
        
        <div class="task-footer">
          <span class="badge" style="background:${isCompleted ? '#dcfce7; color:#15803d;' : '#eff6ff; color:#3b82f6;'}">
            ${isCompleted ? 'Completed ✓' : 'Pending'}
          </span>
          <div style="display:flex; gap:0.5rem;">
            ${!isCompleted ? `<button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.8rem;" onclick="handleCompleteTask('${taskId}')">✓ Complete</button>` : ''}
            <button class="btn btn-danger" style="padding:0.25rem 0.6rem; font-size:0.8rem;" onclick="handleDeleteTask('${taskId}', '${escapeHTML(task.title).replace(/'/g, "\\'")}')">🗑 Delete</button>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Render empty state when no tasks match
   */
  static renderEmptyState() {
    return `
      <div style="grid-column: 1 / -1; text-align:center; padding: 3rem 1rem; background:white; border-radius:var(--radius-md); border:1px dashed var(--border-color);">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📝</div>
        <h3 style="font-weight: 700; color:var(--text-main);">No tasks found</h3>
        <p style="color:var(--text-muted); font-size: 0.9rem; margin-top: 0.25rem;">Use the voice microphone above or add a task manually.</p>
      </div>
    `;
  }
}

/**
  Global Task Action Handlers
 */
async function handleCompleteTask(taskId) {
  const res = await ApiClient.completeTask(taskId);
  if (res.success) {
    showToast('Task marked as completed!', 'success');
    if (window.loadTasks) window.loadTasks();
  } else {
    showToast(res.error || 'Failed to complete task', 'error');
  }
}

async function handleDeleteTask(taskId, taskTitle) {
  if (confirm(`Are you sure you want to delete the task "${taskTitle}"?`)) {
    const res = await ApiClient.deleteTask(taskId);
    if (res.success) {
      showToast('Task deleted successfully', 'info');
      if (window.loadTasks) window.loadTasks();
    } else {
      showToast(res.error || 'Failed to delete task', 'error');
    }
  }
}
