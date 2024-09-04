from typing import List, Optional, Union
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 

from app.schema.default import *
from app.schema.user import *
from app.schema.character import * 

class ChatroomRequestData(BaseModel):
    name: str
    character: CharacterResponseData
    user: UserResponseData

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
                "name": "채팅방 이름",
                "character": {
                    "_id": "고유 ID",
                    "name": "캐릭터 이름",
                    "profile": "캐릭터 프로필 URL",
                    "gender": "성별(male/female/other)",
                    "relationship": "관계",
                    "personality": "성격",
                    "details": "세부사항",
                    "greeting": "첫인사",
                    "summary": "한줄요약",
                    "user": {
                        "username": "user123",
                        "nickname": "apple"
                    },
                    "createDate": "생성날짜",
                    "updateDate": "수정날짜",
                    "userCount": "사용 횟수",
                },
                "user": {
                    "username": "사용자 ID",
                    "nickname": "사용자 닉네임"
                }
            }
        }

class ChatroomData(ChatroomRequestData):
    createDate: datetime 

class ChatroomResponseData(ChatroomData):
    id: str = Field(..., alias="_id")

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
                "name": "채팅방 이름",
                "character": {
                    "_id": "고유 ID",
                    "name": "캐릭터 이름",
                    "profile": "캐릭터 프로필 URL",
                    "gender": "성별(male/female/other)",
                    "relationship": "관계",
                    "personality": "성격",
                    "details": "세부사항",
                    "greeting": "첫인사",
                    "user": {
                        "username": "user123",
                        "nickname": "apple"
                    },
                    "createDate": "생성날짜",
                    "userCount": "사용 횟수"
                },
                "createDate": "채팅방 생성 시간"
            }
        }

        # alias 허용
        populate_by_name = True

class ChatroomResponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str
    data: Union[str,List[ChatroomResponseData]] = []

class ChatroomChatRequest(BaseModel):
    id: str
    name: str
    