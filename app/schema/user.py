from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 
from passlib.context import CryptContext 

from app.schema.default import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

# 회원가입 시 들어오는 데이터
class RegisterData(BaseModel):
    username: str = Field(..., min_length=6, max_length=15, pattern=r"^[A-Za-z0-9]+$")
    nickname: str = Field(..., min_length=1, max_length=15, pattern=r"^[가-힣A-Za-z0-9]+$")
    password: str = Field(..., min_length=8, max_length=15, pattern=r"^[A-Za-z0-9!@#$]+$")

    def hash_password(self):
        self.password = pwd_context.hash(self.password)
    
    class Config:
        # 예시
        json_schema_extra = {
            "example": {
                "username": "user123",
                "nickname": "momomo",
                "password": "asdfgasdfg",
            }
        }

# 로그인 시 들어오는 데이터
class LoginData(BaseModel):
    username: str = Field(..., min_length=6, max_length=15, pattern=r"^[A-Za-z0-9]+$")
    password: str = Field(..., min_length=8, max_length=15, pattern=r"^[A-Za-z0-9!@#$]+$")

    class Config:
        # 예시
        json_schema_extra = {
            "example": {
                "username": "user123",
                "password": "asdfgasdfg",
            }
        }

# DB에 넣을 때 데이터
class UserData(RegisterData):
    username: str
    nickname: str
    password: str 
    createDate: datetime 
    currentDate: Optional[datetime]

# 프론트에 전달해주는 데이터
class UserResponseData(BaseModel):
    username: str = Field(...)
    nickname: str = Field(...)

# 프론트에 전달해주는 메세지
class UserResponse(BaseModel):
    status: Status = Field(default=Status.SUCCESS)
    message: str 
    data: UserResponseData