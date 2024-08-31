from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 

from app.schema.default import *
from app.schema.user import *

class CharacterRequestData(BaseModel):
    name: str
    profile: str 
    gender: Gender
    relationship: str
    personality: str
    details: str
    greeting: str
    user: UserResponseData

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
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
                }
            }
        }

class CharacterData(CharacterRequestData):
    createDate: datetime 
    userCount: int

class CharacterReponseData(CharacterData):
    id: str = Field(..., alias="_id")

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
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
                }
            }
        }

class CharacterReponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str
    data: List[CharacterReponseData]
    