from fastapi import APIRouter, Body
from typing import List

from app.database import mongodb
from app.schema.profile import * 

collection_name = "profile"

router = APIRouter()

@router.get("/", summary="프로필 이미지를 조회합니다")
async def get_profile():
    # Collection 연결
    await mongodb.get_collection(collection_name)

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
async def get_profile(data: List[ProfileData]=Body(...,example=profile_example)):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        success = 0
        fail = 0
        for element in data:
            query = {"img_url": element.img_url}
            data = await mongodb.find_with_query(query)
            if not data:
                await mongodb.insert(insert_data)
                success += 1
            else:
                fail += 1
        
        return SuccessResponse(message=f"✅ Success Add Profile Data: {success} (duplication: {fail})")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Add Profile Data: {e}")
