from fastapi import APIRouter

from app.api.v1.endpoints import user, profile, character, chatroom, chatting

api_router = APIRouter()

api_router.include_router(
    router=user.router,
    prefix="/user",
    tags=["user"]
)

api_router.include_router(
    router=profile.router,
    prefix="/profile",
    tags=["profile"]
)

api_router.include_router(
    router=character.router,
    prefix="/character",
    tags=["character"]
)

api_router.include_router(
    router=chatroom.router,
    prefix="/chatroom",
    tags=["chatroom"]
)

api_router.include_router(
    router=chatting.router,
    prefix="/chatting",
    tags=["chatting"]
)