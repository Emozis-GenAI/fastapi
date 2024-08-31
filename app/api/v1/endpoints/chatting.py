from fastapi import APIRouter, Body

from app.core.logger import logger

router = APIRouter()

@router.get("/{chatroom_id}", summary="특정 채팅방 대화 히스토리를 조회합니다")
async def get_chathistory():
    return ""

@router.post("/", summary="채팅을 DB에 저장합니다")
async def post_chatroom():
    return ""
