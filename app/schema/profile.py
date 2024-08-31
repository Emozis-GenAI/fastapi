from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 

from app.schema.default import *

class Age(str, Enum):
    YOUTH = "youth"
    MIDDLE = "middle_age"
    ELDERLY = "elderly"

class ProfileInsertData(BaseModel):
    img_url: str 
    gender: Gender 
    age: Age

class ProfileData(ProfileInsertData):
    _id: str

class ProfileResponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str
    data: List[ProfileData]


