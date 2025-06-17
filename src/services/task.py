from datetime import date

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)

    try:
        db.commit()
        db.refresh(db_task)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while creating task: {str(e)}",
        )
    return db_task


def get_tasks(
    db: Session, status_filter: str | None = None, due_date_filter: date | None = None
) -> list[Task]:
    query = db.query(Task)

    if status_filter:
        query = query.filter(Task.status == status_filter)

    if due_date_filter:
        query = query.filter(Task.due_date == due_date_filter)

    return query.all()


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task:
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    try:
        db.commit()
        db.refresh(db_task)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while updating task {task_id}: {str(e)}",
        )
    return db_task


def delete_task(db: Session, task_id: int) -> None:
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    try:
        db.delete(db_task)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while deleting task {task_id}: {str(e)}",
        )
