from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field 
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
class Status(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class SuccessResponse(BaseModel):
    status: str = Field(default=Status.SUCCESS)
    message: str

class ErrorResponse(BaseModel):
    status: str = Field(default=Status.FAILURE)
    message: str
