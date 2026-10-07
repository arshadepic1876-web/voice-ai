/**
 * REST API Client for communicating with Flask Backend.
 */
const API_BASE_URL = 'http://127.0.0.1:5000/api';

class ApiClient {
  /**
   * Health check endpoint ping
   */
  static async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (err) {
      console.error('API health check error:', err);
      return { success: false, error: 'Cannot connect to backend server' };
    }
  }

  /**
   * Send audio blob to /api/transcribe
   */
  static async uploadAudio(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    try {
      const response = await fetch(`${API_BASE_URL}/transcribe`, {
        method: 'POST',
        body: formData
      });

      return await response.json();
    } catch (err) {
      console.error('Audio upload failed:', err);
      return { success: false, error: 'Network error during audio upload' };
    }
  }

  /**
   * Fetch task collection
   */
  static async getTasks(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/tasks${queryString ? '?' + queryString : ''}`;

    try {
      const response = await fetch(url);
      return await response.json();
    } catch (err) {
      console.error('Fetch tasks error:', err);
      return { success: false, error: 'Failed to fetch tasks' };
    }
  }

  /**
   * Create task JSON
   */
  static async createTask(taskData) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      });
      return await response.json();
    } catch (err) {
      console.error('Create task error:', err);
      return { success: false, error: 'Failed to create task' };
    }
  }

  /**
   * Update task by ID
   */
  static async updateTask(taskId, taskData) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      });
      return await response.json();
    } catch (err) {
      console.error('Update task error:', err);
      return { success: false, error: 'Failed to update task' };
    }
  }

  /**
   * Mark task complete
   */
  static async completeTask(taskId) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/complete`, {
        method: 'PATCH'
      });
      return await response.json();
    } catch (err) {
      console.error('Complete task error:', err);
      return { success: false, error: 'Failed to mark task complete' };
    }
  }

  /**
   * Delete task by ID
   */
  static async deleteTask(taskId) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'DELETE'
      });
      return await response.json();
    } catch (err) {
      console.error('Delete task error:', err);
      return { success: false, error: 'Failed to delete task' };
    }
  }
}

