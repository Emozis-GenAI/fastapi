from fastapi import APIRouter, Body

from app.core.logger import logger

router = APIRouter()

@router.post("/signup", summary="회원가입")
async def signup():
    return ""

@router.post("/login", summary="로그인")
async def login():
    return ""
    
    

    