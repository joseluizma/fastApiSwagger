from pydantic import BaseModel
from typing import Optional

class ServiceCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Service(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: int