from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None