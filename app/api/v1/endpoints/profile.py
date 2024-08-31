from fastapi import APIRouter, Body

from app.core.logger import logger

router = APIRouter()

@router.get("/", summary="프로필 이미지를 조회합니다")
async def get_profile():
    return ""
