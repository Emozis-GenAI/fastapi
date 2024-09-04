from fastapi import APIRouter, Body

from app.langchain.summary import summarybot
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
        query = {"user": user.dict()}
        data = await mongodb.find_with_query(query)

        if isinstance(data, dict):
            data = [data]
        
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
    summary = await summarybot.ainvoke(data.details)

    try:
        insert_data = CharacterData(
            **data.dict(),
            summary=summary,
            createDate=datetime.now(),
            userCount=0
        )
        response = await mongodb.insert(insert_data.dict())
        return SuccessResponse(message=f"✅ Success Create Character: {response[0]}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Create Character: {e}")

@router.put("/count", summary="캐릭터 조회 수를 업데이트 합니다.")
async def post_character(data: CharacterCountRequestData):
    # Collection 연결
    await mongodb.get_collection(collection_name)
    
    try:
        await mongodb.update(data.id, data.dict())
        return SuccessResponse(message=f"✅ Success Update UserCount: {data.userCount}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Update UserCount: {e}")

@router.put("/", summary="캐릭터 정보를 수정합니다")
async def put_character(data: CharacterResponseData):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        await mongodb.update(data.id, data.dict())
        return SuccessResponse(message=f"✅ Success Update Character: {data.id}")
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

@router.get("/test")
async def test():
    request = "동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라만세"
    result = await summarybot.ainvoke(request)
    return result