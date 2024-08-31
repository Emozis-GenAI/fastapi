from fastapi import APIRouter, Body

from app.core.logger import logger

router = APIRouter()

@router.get("/", summary="채팅방 정보를 조회합니다")
async def get_chatroom():
    return ""

@router.get("/{id}", summary="특정 채팅방 정보를 조회합니다")
async def get_chatroom_one():
    return ""

@router.post("/", summary="채팅방을 생성합니다")
async def post_chatroom():
    return ""

@router.put("/", summary="채팅방 정보를 수정합니다")
async def put_chatroom():
    return ""

@router.delete("/{id}", summary="특정 채팅방을 삭제합니다")
async def del_chatroom(id: str):
    return ""