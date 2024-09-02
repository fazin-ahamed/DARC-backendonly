from pydantic import BaseModel
from typing import Optional

class FileSchema(BaseModel):
    filename: str
    content: Optional[str] = None
    language: Optional[str] = None

class MessageSchema(BaseModel):
    sender: str
    message: str
