from typing import Optional

from databases.business_todo.src.repositories.user_repo import UserRepository
from databases.business_todo.src.utils.validators import (
    validate_name, validate_phone, validate_user_id,
    ValidationError
)


class UserService:

    @staticmethod
    def get_me(user_id: int) -> dict:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found")
        return {k: v for k, v in user.items() if k != "password_hash"}

    @staticmethod
    def get_users(role: Optional[str] = None, status: Optional[str] = None,
                  current_user: dict = None) -> list:
        if current_user["role"] != "admin":
            if role == "executor":
                return UserRepository.get_all(role="executor", status="active")
            raise ValidationError("Not enough permissions")

        return UserRepository.get_all(role=role, status=status)

    @staticmethod
    def update_user(user_id: int, update_data: dict, current_user: dict) -> dict:
        user_id = validate_user_id(user_id)

        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found")
        if current_user["role"] != "admin" and current_user["user_id"] != user_id:
            raise ValidationError("Not enough permissions")
        validated = {}

        if "first_name" in update_data and update_data["first_name"] is not None:
            validated["first_name"] = validate_name(update_data["first_name"], "First name")

        if "last_name" in update_data and update_data["last_name"] is not None:
            validated["last_name"] = validate_name(update_data["last_name"], "Last name")

        if "phone" in update_data:
            validated["phone"] = validate_phone(update_data["phone"])

        if "status" in update_data and current_user["role"] == "admin":
            validated["status"] = update_data["status"]

        if not validated:
            return {k: v for k, v in user.items() if k != "password_hash"}

        updated = UserRepository.update(user_id, **validated)
        return {k: v for k, v in updated.items() if k != "password_hash"}