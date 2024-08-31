from fastapi import APIRouter, Body
from typing import List

from app.database import mongodb
from app.schema.profile import * 

mongodb.set_collection("profile")

router = APIRouter()

@router.get("/", summary="프로필 이미지를 조회합니다")
async def get_profile():
    try:
        data = await mongodb.find_all()
        return ProfileResponse(
            message=f"✅ Success Retrieve Profile Data: {len(data)}",
            data=data
        )
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Retrieve Profile Data: {e}")

profile_example = [
    {
        "img_url": "...",
        "gender": "male",
        "age": "youth"
    },
    {
        "img_url": "...",
        "gender": "female",
        "age": "elderly"
    }
]

@router.post("/", summary="프로필 이미지를 추가합니다")
async def get_profile(data: List[ProfileInsertData]=Body(...,example=profile_example)):
    insert_data = [element.dict() for element in data]
    try:
        response = await mongodb.insert(insert_data)
        return SuccessResponse(message=f"✅ Success Add Profile Data: {len(response)}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Add Profile Data: {e}")
