from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 

from app.schema.default import *
from app.schema.user import *
from app.schema.chatroom import *

from app.langchain.chatbot import chatbot

class ChatRole(str, Enum):
    CHARACTER = "assistant"
    USER = "user"

class ChatRequestData(BaseModel):
    chatroom: ChatroomChatRequest
    role: ChatRole
    content: str

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
                "chatroom": {
                    "id": "dddd",
                    "name": "채팅방 이름",
                },
                "role": "assistant",
                "content": "안녕"
            }
        }

        # alias 허용
        populate_by_name = True

class ChatData(ChatRequestData):
    createDate: datetime

class ChatResponseData(ChatData):
    id: str = Field(..., alias="_id")

class ChatHistoryResponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str
    data: List[ChatResponseData] = []

