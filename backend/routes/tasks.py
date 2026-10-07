from flask import Blueprint, request
from utils.errors import api_response, error_response
from services.task_service import TaskService

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    GET /api/tasks
    Query parameters:
    - filter: 'all', 'today', 'upcoming', 'overdue', 'urgent', 'high_priority', 'completed', 'pending'
    - category: 'College', 'Study', 'Work', etc.
    - q: search query string
    """
    filter_by = request.args.get('filter')
    category = request.args.get('category')
    search_query = request.args.get('q')
    
    result = TaskService.get_all_tasks(filter_by=filter_by, category=category, search_query=search_query)
    
    return api_response(
        success=True,
        data=result,
        message="Tasks retrieved successfully",
        status_code=200
    )

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """POST /api/tasks - Create a new structured task."""
    data = request.get_json()
    if not data or 'title' not in data or not data['title'].strip():
        return error_response("Task title is required", status_code=400)
        
    new_task = TaskService.create_task(data)
    
    return api_response(
        success=True,
        data=new_task,
        message="Task created successfully",
        status_code=201
    )

@tasks_bp.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """GET /api/tasks/<task_id> - Retrieve single task by ID."""
    task = TaskService.get_task_by_id(task_id)
    if not task:
        return error_response(f"Task with ID '{task_id}' not found", status_code=404)
        
    return api_response(
        success=True,
        data=task,
        message="Task retrieved successfully",
        status_code=200
    )

@tasks_bp.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """PUT /api/tasks/<task_id> - Update existing task details."""
    data = request.get_json()
    if not data:
        return error_response("Request body payload missing", status_code=400)
        
    updated = TaskService.update_task(task_id, data)
    if not updated:
        return error_response(f"Task with ID '{task_id}' not found", status_code=404)
        
    return api_response(
        success=True,
        data=updated,
        message="Task updated successfully",
        status_code=200
    )

@tasks_bp.route('/api/tasks/<task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """PATCH /api/tasks/<task_id>/complete - Mark task status as completed."""
    completed = TaskService.complete_task(task_id)
    if not completed:
        return error_response(f"Task with ID '{task_id}' not found", status_code=404)
        
    return api_response(
        success=True,
        data=completed,
        message="Task marked as completed",
        status_code=200
    )

@tasks_bp.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """DELETE /api/tasks/<task_id> - Delete task by ID."""
    success = TaskService.delete_task(task_id)
    if not success:
        return error_response(f"Task with ID '{task_id}' not found", status_code=404)
        
    return api_response(
        success=True,
        data={"deleted_task_id": task_id},
        message="Task deleted successfully",
        status_code=200
    )
