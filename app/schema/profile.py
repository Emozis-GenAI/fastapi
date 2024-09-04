from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 

from app.schema.default import *

class Age(str, Enum):
    YOUTH = "youth"
    MIDDLE = "middle_age"
    ELDERLY = "elderly"
    ETC = "etc"

class ProfileData(BaseModel):
    img_url: str 
    gender: Gender 
    age: Age

class ProfileResponseData(ProfileData):
    id: str = Field(..., alias="_id")

class ProfileResponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str
    data: List[ProfileResponseData]


