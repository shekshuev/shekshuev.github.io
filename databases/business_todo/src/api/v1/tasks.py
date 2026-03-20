from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from databases.business_todo.src.services.task_service import TaskService
from databases.business_todo.src.utils.validators import ValidationError
from databases.business_todo.src.api.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
def get_tasks(
        status: Optional[str] = None,
        priority: Optional[str] = None,
        customer_id: Optional[str] = None,
        executor_id: Optional[str] = None,
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        current_user: dict = Depends(get_current_user)
):
    try:
        cid = int(customer_id) if customer_id and customer_id != "me" else (
            current_user["user_id"] if customer_id == "me" else None)
        eid = int(executor_id) if executor_id and executor_id != "me" else (
            current_user["user_id"] if executor_id == "me" else None)

        return TaskService.get_tasks(
            status=status,
            priority=priority,
            customer_id=cid,
            executor_id=eid,
            page=page,
            limit=limit
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={e.field: e.message} if e.field else e.message)


@router.post("")
def create_task(
        request: dict,
        current_user: dict = Depends(get_current_user)
):
    try:
        return TaskService.create_task(
            task_text=request.get("task_text"),
            description=request.get("description"),
            priority=request.get("priority"),
            payment=request.get("payment"),
            deadline=request.get("deadline"),
            current_user=current_user
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={e.field: e.message} if e.field else e.message)


@router.get("/{task_id}")
def get_task(
        task_id: int,
        current_user: dict = Depends(get_current_user)
):
    try:
        return TaskService.get_task(task_id, current_user)
    except ValidationError as e:
        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)


@router.put("/{task_id}")
def update_task(
        task_id: int,
        request: dict,
        current_user: dict = Depends(get_current_user)
):
    try:
        return TaskService.update_task(task_id, request, current_user)
    except ValidationError as e:
        status_code = 404 if "not found" in e.message.lower() else 403 if "permission" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail={e.field: e.message} if e.field else e.message)


@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        current_user: dict = Depends(get_current_user)
):
    try:
        return TaskService.delete_task(task_id, current_user)
    except ValidationError as e:
        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)