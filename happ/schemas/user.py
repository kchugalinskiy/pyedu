from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    email: str


class UserUpdate(BaseModel):
    id: int
    full_name: Optional[str]
    email: Optional[str]
