import pytest
from unittest.mock import patch
from databases.business_todo.src.services.task_service import TaskService
from databases.business_todo.src.utils.validators import ValidationError


class TestTaskService:

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_create_task_empty_text(self, mock_repo):
        mock_user = {"user_id": 1, "role": "customer"}
        with pytest.raises(ValidationError):
            TaskService.create_task(
                task_text="",
                priority="low",
                payment=100,
                current_user=mock_user
            )

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_create_task_negative_payment(self, mock_repo):
        mock_user = {"user_id": 1, "role": "customer"}
        with pytest.raises(ValidationError):
            TaskService.create_task(
                task_text="Test task",
                priority="low",
                payment=-50,
                current_user=mock_user
            )

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_create_task_wrong_role(self, mock_repo):
        mock_user = {"user_id": 1, "role": "executor"}
        with pytest.raises(ValidationError, match="Not enough permissions"):
            TaskService.create_task(
                task_text="Test task",
                priority="low",
                payment=100,
                current_user=mock_user
            )

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_get_task_not_found(self, mock_repo):
        mock_repo.get_by_id.return_value = None
        mock_user = {"user_id": 1, "role": "customer"}

        with pytest.raises(ValidationError, match="Task not found"):
            TaskService.get_task(task_id=999, current_user=mock_user)

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_get_task_permission_executor(self, mock_repo):
        mock_task = {
            "task_id": 1,
            "executor_id": 5,
            "customer_id": 2,
            "status": "new"
        }
        mock_repo.get_by_id.return_value = mock_task
        mock_user = {"user_id": 1, "role": "executor"}

        with pytest.raises(ValidationError, match="Not enough permissions"):
            TaskService.get_task(task_id=1, current_user=mock_user)

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_delete_task_permission(self, mock_repo):
        mock_task = {
            "task_id": 1,
            "customer_id": 5,
            "executor_id": None
        }
        mock_repo.get_by_id.return_value = mock_task
        mock_user = {"user_id": 1, "role": "customer"}

        with pytest.raises(ValidationError, match="Not enough permissions"):
            TaskService.delete_task(task_id=1, current_user=mock_user)

    @patch('databases.business_todo.src.services.task_service.TaskRepository')
    def test_update_task_success(self, mock_repo):
        mock_task = {
            "task_id": 1,
            "customer_id": 1,
            "executor_id": None,
            "status": "new",
            "priority": "low"
        }
        mock_repo.get_by_id.return_value = mock_task
        mock_repo.update.return_value = {**mock_task, "priority": "high"}

        mock_user = {"user_id": 1, "role": "customer"}
        update_data = {"priority": "high"}

        result = TaskService.update_task(task_id=1, update_data=update_data, current_user=mock_user)

        assert result["priority"] == "high"
        mock_repo.update.assert_called_once()