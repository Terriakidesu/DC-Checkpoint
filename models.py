from pydantic import BaseModel
from typing import Optional


class Guild(BaseModel):
    id: str
    name: str


class Channel(BaseModel):
    id: str
    type: Optional[str]
    name: Optional[str] = None
    guild: Optional[Guild] = None


class Message(BaseModel):
    ID: int
    Timestamp: str
    Contents: Optional[str]
    Attachments: Optional[str]
