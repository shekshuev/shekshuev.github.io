from typing import Optional, List
from datetime import datetime

from databases.business_todo.src.db.context import get_db_cursor
from databases.business_todo.src.core.security import get_password_hash


class UserRepository:
    @staticmethod
    def get_by_email(email: str) -> Optional[dict]:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            return cursor.fetchone()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[dict]:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT user_id, first_name, last_name, email, phone, role, status, created_at FROM users WHERE user_id = %s",
                (user_id,)
            )
            return cursor.fetchone()

    @staticmethod
    def create(first_name: str, last_name: str, email: str, password: str, phone: Optional[str], role: str) -> dict:
        password_hash = get_password_hash(password)
        with get_db_cursor() as cursor:
            cursor.execute(
                """INSERT INTO users (first_name, last_name, email, password_hash, phone, role, status, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, 'active', %s)
                   RETURNING user_id, first_name, last_name, email, phone, role, status, created_at""",
                (first_name, last_name, email, password_hash, phone, role, datetime.utcnow())
            )
            return cursor.fetchone()

    @staticmethod
    def update(user_id: int, **kwargs) -> Optional[dict]:
        if not kwargs:
            return UserRepository.get_by_id(user_id)

        fields = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]

        with get_db_cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET {fields} WHERE user_id = %s RETURNING user_id, first_name, last_name, email, phone, role, status, created_at",
                values
            )
            return cursor.fetchone()

    @staticmethod
    def get_all(role: Optional[str] = None, status: Optional[str] = None) -> List[dict]:
        query = "SELECT user_id, first_name, last_name, email, phone, role, status, created_at FROM users WHERE 1=1"
        params = []

        if role:
            query += " AND role = %s"
            params.append(role)
        if status:
            query += " AND status = %s"
            params.append(status)

        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()