from fastapi import APIRouter, Body

from app.core.logger import logger

router = APIRouter()

@router.get("/", summary="캐릭터 정보를 조회합니다")
async def get_character():
    return ""

@router.get("/{id}", summary="특정 캐릭터 정보를 조회합니다")
async def get_character_one(id: str):
    return ""

@router.post("/", summary="캐릭터 정보를 생성합니다")
async def post_character():
    return ""

@router.post("/", summary="캐릭터 정보를 수정합니다")
async def put_character():
    return ""

@router.delete("/{id}", summary="특정 캐릭터 정보를 삭제합니다")
async def del_character(id: str):
    return ""