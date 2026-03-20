import json
from unittest.mock import patch

from databases.business_todo.src.utils.validators import ValidationError
from databases.business_todo.tests.conftest import create_test_token


def test_create_task_success(client):
    token = create_test_token(user_id=1, role="customer")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "task_text": "Найти кота",
        "priority": "low",
        "payment": 500,
        "description": "Рыжий"
    }

    with patch('backend.src.api.v1.tasks.TaskService') as mock_service:
        mock_service.create_task.return_value = {
            "task_id": 1,
            "task_text": "Найти кота",
            "status": "new"
        }

        response = client.post('/api/v1/tasks/', json=payload, headers=headers)

        assert response.status_code in [200, 201]
        data = response.json()
        assert data['task_text'] == "Найти кота"


def test_create_task_validation_error(client):
    token = create_test_token(user_id=1, role="customer")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"task_text": "", "priority": "low", "payment": 100}

    with patch('backend.src.api.v1.tasks.TaskService') as mock_service:
        mock_service.create_task.side_effect = ValidationError("Invalid data")

        response = client.post('/api/v1/tasks/', json=payload, headers=headers)

        assert response.status_code == 400


def test_get_tasks_success(client):
    token = create_test_token(user_id=1, role="customer")
    headers = {"Authorization": f"Bearer {token}"}

    with patch('backend.src.api.v1.tasks.TaskService') as mock_service:
        mock_service.get_tasks.return_value = {"tasks": [], "total": 0}

        response = client.get('/api/v1/tasks/', headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data


def test_get_task_not_found(client):
    token = create_test_token(user_id=1, role="customer")
    headers = {"Authorization": f"Bearer {token}"}

    with patch('backend.src.api.v1.tasks.TaskService') as mock_service:
        mock_service.get_task.side_effect = ValidationError("Task not found")

        response = client.get('/api/v1/tasks/999', headers=headers)

        assert response.status_code == 404


def test_delete_task_success(client):
    token = create_test_token(user_id=3, role="admin")
    headers = {"Authorization": f"Bearer {token}"}

    with patch('backend.src.api.v1.tasks.TaskService') as mock_service:
        mock_service.create_task.return_value = {"task_id": 1}
        mock_service.delete_task.return_value = {"message": "Task deleted"}

        client.post('/api/v1/tasks/', json={
            "task_text": "Test", "priority": "low", "payment": 100
        }, headers=headers)

        response = client.delete('/api/v1/tasks/1', headers=headers)

        assert response.status_code == 200