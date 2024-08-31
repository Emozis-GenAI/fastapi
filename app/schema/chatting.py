from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 

from app.schema.default import *
from app.schema.user import *

class ChatRole(str, Enum):
    CHARACTER = "character"
    USER = "user"

class ChatRequestData(BaseModel):
    chatroom_id: str
    user: UserResponseData
    role: ChatRole
    content: str

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
                "chatroom_id": "asdfjiejfkal",
                "user": {
                    "username": "user123",
                    "nickname": "hello"
                },
                "role": "character",
                "content": "안녕"
            }
        }

class ChatData(ChatRequestData):
    createDate: datetime

class ChatResponseData(ChatData):
    _id: str

class ChatHistoryResponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str
    data: List[ChatData]

