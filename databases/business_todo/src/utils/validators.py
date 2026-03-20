import re
from datetime import datetime

class ValidationError(Exception):
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)

def validate_email(email: str) -> str:
    if not email:
        raise ValidationError("Email is required", "email")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format", "email")
    return email.strip().lower()

def validate_password(password: str) -> str:
    if not password:
        raise ValidationError("Password is required", "password")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters", "password")
    if len(password) > 72:
        raise ValidationError("Password must not exceed 72 characters", "password")
    return password

def validate_name(value: str, field_name: str) -> str:
    if not value:
        raise ValidationError(f"{field_name} is required", field_name)
    if len(value) < 2 or len(value) > 50:
        raise ValidationError(f"{field_name} must be between 2 and 50 characters", field_name)
    return value.strip()

def validate_task_text(text: str) -> str:
    if not text:
        raise ValidationError("Task text is required", "task_text")
    if len(text) < 5 or len(text) > 200:
        raise ValidationError("Task text must be between 5 and 200 characters", "task_text")
    return text.strip()

def validate_description(description: str) -> str:
    if description and len(description) > 2000:
        raise ValidationError("Description must be less than 2000 characters", "description")
    return description.strip() if description else None

def validate_payment(payment) -> float:
    try:
        payment = float(payment)
        if payment <= 0:
            raise ValidationError("Payment must be greater than 0", "payment")
        return payment
    except (TypeError, ValueError):
        raise ValidationError("Payment must be a valid number", "payment")

def validate_priority(priority: str) -> str:
    valid = ["low", "medium", "high", "urgent"]
    if priority not in valid:
        raise ValidationError(f"Priority must be one of: {', '.join(valid)}", "priority")
    return priority

def validate_status(status: str) -> str:
    valid = ["new", "assigned", "in_progress", "completed", "cancelled"]
    if status not in valid:
        raise ValidationError(f"Status must be one of: {', '.join(valid)}", "status")
    return status

def validate_role(role: str) -> str:
    valid = ["admin", "customer", "executor"]
    if role not in valid:
        raise ValidationError(f"Role must be one of: {', '.join(valid)}", "role")
    return role

def validate_phone(phone: str) -> str:
    if phone and len(phone) > 20:
        raise ValidationError("Phone must be less than 20 characters", "phone")
    return phone.strip() if phone else None

def validate_comment_text(text: str) -> str:
    if not text:
        raise ValidationError("Comment text is required", "text")
    if len(text) < 1 or len(text) > 1000:
        raise ValidationError("Comment text must be between 1 and 1000 characters", "text")
    return text.strip()

def validate_deadline(deadline) -> str:
    if not deadline:
        return None
    try:
        if isinstance(deadline, str):
            datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        return deadline
    except (ValueError, AttributeError):
        raise ValidationError("Deadline must be a valid ISO date format", "deadline")

def validate_user_id(user_id) -> int:
    try:
        uid = int(user_id)
        if uid <= 0:
            raise ValidationError("Invalid user ID", "user_id")
        return uid
    except (TypeError, ValueError):
        raise ValidationError("User ID must be a valid integer", "user_id")

def validate_task_id(task_id) -> int:
    try:
        tid = int(task_id)
        if tid <= 0:
            raise ValidationError("Invalid task ID", "task_id")
        return tid
    except (TypeError, ValueError):
        raise ValidationError("Task ID must be a valid integer", "task_id")