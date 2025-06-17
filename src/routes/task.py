from datetime import date

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.logger import logger
from src.database.database import get_db
from src.models.task import TaskStatus
from src.schemas.task import TaskCreate, TaskOut, TaskUpdate
from src.services.task import create_task, delete_task, get_tasks, update_task

router = APIRouter()


@router.post("/tasks", response_model=TaskOut, status_code=201)
def create(task: TaskCreate, db: Session = Depends(get_db), request: Request = None):
    logger.info(f"{request.method} {request.url}")
    created_task = create_task(db, task)
    return created_task


@router.get("/tasks", response_model=list[TaskOut])
def read_all(
    status: TaskStatus | None = None,
    due_date: date | None = None,
    db: Session = Depends(get_db),
    request: Request = None,
):
    logger.info(f"{request.method} {request.url} | status={status} due_date={due_date}")
    return get_tasks(db, status_filter=status, due_date_filter=due_date)


@router.put("/tasks/{task_id}", response_model=TaskOut)
def update(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    request: Request = None,
):
    logger.info(f"{request.method} {request.url}")
    updated_task = update_task(db, task_id, task)
    return updated_task


@router.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: int, db: Session = Depends(get_db), request: Request = None):
    logger.info(f"{request.method} {request.url}")
    delete_task(db, task_id)
