from fastapi import APIRouter, HTTPException, Depends
from databases.business_todo.src.services.auth_service import AuthService
from databases.business_todo.src.utils.validators import ValidationError
from databases.business_todo.src.api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(request: dict):
    try:
        return AuthService.login(
            email=request.get("email"),
            password=request.get("password")
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={e.field: e.message} if e.field else e.message)

@router.post("/register")
def register(request: dict):
    try:
        return AuthService.register(
            first_name=request.get("first_name"),
            last_name=request.get("last_name"),
            email=request.get("email"),
            password=request.get("password"),
            phone=request.get("phone"),
            role=request.get("role", "customer")
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={e.field: e.message} if e.field else e.message)

@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    try:
        return AuthService.logout(current_user["user_id"])
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.post("/refresh")
def refresh(request: dict):
    try:
        return AuthService.refresh_token(request.get("refreshToken"))
    except ValidationError as e:
        raise HTTPException(status_code=401, detail=e.message)