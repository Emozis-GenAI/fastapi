from fastapi import APIRouter, Body

from app.core.logger import logger
from app.database import mongodb

router = APIRouter()

@router.get("/", summary="MongoDB Collection 목록을 조회합니다")
async def get_collection():
    collection_list = await mongodb.manage_collection(method="get")
    return collection_list

@router.post("/{collection_name}", summary="MongoDB Collection을 생성합니다")
async def post_collection(collection_name: str):
    message = await mongodb.manage_collection(collection_name, method="create")
    return message

@router.delete("/{collection_name}", summary="MongoDB Collection을 삭제합니다")
async def del_collection(collection_name: str):
    message =  await mongodb.manage_collection(collection_name, method="drop")
    return message