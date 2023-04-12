from pydantic import BaseModel
from typing import Optional


class HelloRequest(BaseModel):
    name: str


class GoodbyeRequest(BaseModel):
    name: str


class HelloResponse(BaseModel):
    message: str


class GoodbyeResponse(BaseModel):
    message: str
    hello_count: Optional[int]
