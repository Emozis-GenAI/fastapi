from fastapi import APIRouter, Body

from app.database import mongodb
from app.schema.character import *

collection_name = "character"

router = APIRouter()

@router.get("/", summary="캐릭터 정보를 조회합니다")
async def get_character():
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        data = await mongodb.find_all()
        
        return CharacterResponse(
            message=f"✅ Success Retrieve Character Data: {len(data)}",
            data=data
        )
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Retrieve Character Data: {e}")


@router.get("/user", summary="특정 유저가 만든 캐릭터 정보를 조회합니다")
async def get_character_one(user: UserResponseData):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        query = {"user": user}
        data = await mongodb.find_with_query(query)
        
        return CharacterResponse(
            message=f"✅ Success Retrieve User Chat List: {len(data)}",
            data=data
        )
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Retrieve User Chat List: {e}")

@router.post("/", summary="캐릭터 정보를 생성합니다")
async def post_character(data: CharacterRequestData):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        insert_data = CharacterData(
            **data.dict(),
            createDate=datetime.now(),
            userCount=0
        )
        await mongodb.insert(insert_data.dict())
        return SuccessResponse(message=f"✅ Success Create Character: {data['_id']}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Create Character: {e}")

@router.put("/", summary="캐릭터 정보를 수정합니다")
async def put_character(data: CharacterReponseData):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        await mongodb.update(id, data)
        return SuccessResponse(message=f"✅ Success Update Character: {data['_id']}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Update Character: {e}")

@router.delete("/{id}", summary="특정 캐릭터 정보를 삭제합니다")
async def del_character(id: str):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        await mongodb.delete(id)
        return SuccessResponse(message=f"✅ Success Delete Character: {id}")
    except Exception as e:
        return ErrorResponse(message=f"❌")