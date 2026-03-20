from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from databases.business_todo.src.services.user_service import UserService
from databases.business_todo.src.utils.validators import ValidationError
from databases.business_todo.src.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    try:
        return UserService.get_me(current_user["user_id"])
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=e.message)

@router.get("")
def get_users(
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    try:
        return UserService.get_users(role=role, status=status, current_user=current_user)
    except ValidationError as e:
        status_code = 403 if "permission" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail=e.message)

@router.put("/{user_id}")
def update_user(
    user_id: int,
    request: dict,
    current_user: dict = Depends(get_current_user)
):
    try:
        return UserService.update_user(user_id, request, current_user)
    except ValidationError as e:
        status_code = 404 if "not found" in e.message.lower() else 403 if "permission" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail={e.field: e.message} if e.field else e.message)