from typing import Optional

from databases.business_todo.src.repositories.task_repo import TaskRepository
from databases.business_todo.src.utils.validators import (
    validate_task_text, validate_description, validate_priority,
    validate_payment, validate_status, validate_deadline,
    validate_user_id, validate_task_id, ValidationError
)


class TaskService:

    @staticmethod
    def get_tasks(
            status: Optional[str] = None,
            priority: Optional[str] = None,
            customer_id: Optional[int] = None,
            executor_id: Optional[int] = None,
            page: int = 1,
            limit: int = 20
    ) -> dict:
        if status:
            status = validate_status(status)
        if priority:
            priority = validate_priority(priority)

        tasks, total = TaskRepository.get_all(
            status=status,
            priority=priority,
            customer_id=customer_id,
            executor_id=executor_id,
            page=page,
            limit=limit
        )

        for task in tasks:
            if task.get("customer_first_name"):
                task["customer"] = {
                    "user_id": task["customer_id"],
                    "first_name": task["customer_first_name"],
                    "last_name": task["customer_last_name"],
                    "email": task["customer_email"]
                }
                del task["customer_first_name"]
                del task["customer_last_name"]
                del task["customer_email"]

            if task.get("executor_first_name"):
                task["executor"] = {
                    "user_id": task["executor_id"],
                    "first_name": task["executor_first_name"],
                    "last_name": task["executor_last_name"],
                    "email": task["executor_email"]
                }
                del task["executor_first_name"]
                del task["executor_last_name"]
                del task["executor_email"]

        return {
            "tasks": tasks,
            "total": total,
            "page": page,
            "limit": limit
        }

    @staticmethod
    def get_task(task_id: int, current_user: dict) -> dict:
        task_id = validate_task_id(task_id)

        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise ValidationError("Task not found")

        # permission check
        if current_user["role"] == "executor" and task["executor_id"] != current_user["user_id"]:
            raise ValidationError("Not enough permissions")

        if task.get("customer_first_name"):
            task["customer"] = {
                "user_id": task["customer_id"],
                "first_name": task["customer_first_name"],
                "last_name": task["customer_last_name"],
                "email": task["customer_email"]
            }
            del task["customer_first_name"]
            del task["customer_last_name"]
            del task["customer_email"]

        if task.get("executor_first_name"):
            task["executor"] = {
                "user_id": task["executor_id"],
                "first_name": task["executor_first_name"],
                "last_name": task["executor_last_name"],
                "email": task["executor_email"]
            }
            del task["executor_first_name"]
            del task["executor_last_name"]
            del task["executor_email"]

        return task

    @staticmethod
    def create_task(task_text: str, priority: str, payment: float,
                    description: str = None, deadline: str = None,
                    current_user: dict = None) -> dict:
        if current_user["role"] not in ["admin", "customer"]:
            raise ValidationError("Not enough permissions to create tasks")

        task_text = validate_task_text(task_text)
        priority = validate_priority(priority)
        payment = validate_payment(payment)
        description = validate_description(description)
        deadline = validate_deadline(deadline)

        task = TaskRepository.create(
            task_text=task_text,
            description=description,
            customer_id=current_user["user_id"],
            priority=priority,
            payment=payment,
            deadline=deadline
        )
        return task

    @staticmethod
    def update_task(task_id: int, update_data: dict, current_user: dict) -> dict:
        task_id = validate_task_id(task_id)

        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise ValidationError("Task not found")

        # permission logic
        if current_user["role"] == "admin":
            allowed_fields = ["task_text", "description", "priority", "payment",
                              "deadline", "executor_id", "status"]
        elif current_user["role"] == "customer":
            if task["customer_id"] != current_user["user_id"]:
                raise ValidationError("Not your task")
            allowed_fields = ["task_text", "description", "priority", "payment", "deadline"]
        elif current_user["role"] == "executor":
            if task["executor_id"] != current_user["user_id"]:
                raise ValidationError("Not your task")
            allowed_fields = ["status"]
        else:
            raise ValidationError("Not enough permissions")

        # validate and filter fields
        validated = {}

        if "task_text" in update_data and update_data["task_text"] is not None:
            validated["task_text"] = validate_task_text(update_data["task_text"])
            if "task_text" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if "description" in update_data:
            validated["description"] = validate_description(update_data["description"])
            if "description" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if "priority" in update_data and update_data["priority"] is not None:
            validated["priority"] = validate_priority(update_data["priority"])
            if "priority" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if "payment" in update_data and update_data["payment"] is not None:
            validated["payment"] = validate_payment(update_data["payment"])
            if "payment" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if "deadline" in update_data:
            validated["deadline"] = validate_deadline(update_data["deadline"])
            if "deadline" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if "executor_id" in update_data and update_data["executor_id"] is not None:
            validated["executor_id"] = validate_user_id(update_data["executor_id"])
            if "executor_id" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if "status" in update_data and update_data["status"] is not None:
            validated["status"] = validate_status(update_data["status"])
            if "status" not in allowed_fields:
                raise ValidationError("Cannot update this field")

        if not validated:
            return task

        return TaskRepository.update(task_id, **validated)

    @staticmethod
    def delete_task(task_id: int, current_user: dict) -> dict:
        task_id = validate_task_id(task_id)

        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise ValidationError("Task not found")

        if current_user["role"] != "admin" and task["customer_id"] != current_user["user_id"]:
            raise ValidationError("Not enough permissions")

        TaskRepository.delete(task_id)
        return {"message": "Task deleted"}