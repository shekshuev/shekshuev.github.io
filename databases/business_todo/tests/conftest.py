import sys
from pathlib import Path
from datetime import datetime, timedelta
import jwt
import pytest
import os
from starlette.testclient import TestClient

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

os.environ["DB_NAME"] = "test_task_pool"

from databases.business_todo.src.main import app
from databases.business_todo.src.core.config import get_settings

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def create_test_token(user_id: int = 1, role: str = "customer"):
    settings = get_settings()
    payload = {
        "sub": str(user_id),
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@pytest.fixture
def auth_headers():
    token = create_test_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }