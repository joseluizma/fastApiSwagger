from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: int