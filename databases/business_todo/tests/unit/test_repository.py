import pytest
from unittest.mock import patch, MagicMock
from databases.business_todo.src.repositories.task_repo import TaskRepository
from databases.business_todo.src.repositories.user_repo import UserRepository


class TestUserRepository:

    @patch('databases.business_todo.src.repositories.user_repo.get_db_cursor')
    def test_get_by_id(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'user_id': 1, 'email': 'test@test.com', 'status': 'active'}
        mock_cursor_factory.return_value = mock_cursor

        user = UserRepository.get_by_id(1)
        assert user['user_id'] == 1

    @patch('databases.business_todo.src.repositories.user_repo.get_db_cursor')
    def test_get_by_id_not_found(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_cursor_factory.return_value = mock_cursor

        user = UserRepository.get_by_id(999)
        assert user is None

class TestTaskRepository:

    @patch('databases.business_todo.src.repositories.task_repo.get_db_cursor')
    def test_get_by_id(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'task_id': 1, 'task_text': 'Test'}
        mock_cursor_factory.return_value = mock_cursor

        task = TaskRepository.get_by_id(1)
        assert task['task_id'] == 1

    @patch('databases.business_todo.src.repositories.task_repo.get_db_cursor')
    def test_get_all(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'task_id': 1}]
        mock_cursor.fetchone.return_value = {'count': 1}
        mock_cursor_factory.return_value = mock_cursor

        tasks, total = TaskRepository.get_all(page=1, limit=20)
        assert isinstance(tasks, list)
        assert total == 1

    @patch('databases.business_todo.src.repositories.task_repo.get_db_cursor')
    def test_create_task(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'task_id': 1, 'status': 'new'}
        mock_cursor_factory.return_value = mock_cursor

        task = TaskRepository.create(
            task_text='Test',
            description='Desc',
            customer_id=1,
            priority='low',
            payment=100,
            deadline=None
        )
        assert task['status'] == 'new'

    @patch('databases.business_todo.src.repositories.task_repo.get_db_cursor')
    def test_update_task(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'task_id': 1, 'status': 'in_progress'}
        mock_cursor_factory.return_value = mock_cursor

        task = TaskRepository.update(1, status='in_progress')
        assert task['status'] == 'in_progress'

    @patch('databases.business_todo.src.repositories.task_repo.get_db_cursor')
    def test_delete_task(self, mock_cursor_factory):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.rowcount = 1
        mock_cursor_factory.return_value = mock_cursor

        result = TaskRepository.delete(1)
        assert result is True