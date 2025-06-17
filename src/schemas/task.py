from datetime import date

from src.models.task import TaskStatus
from src.schemas.base_model import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    status: TaskStatus = TaskStatus.pending


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
