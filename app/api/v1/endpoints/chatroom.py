from fastapi import APIRouter, Body

from app.schema.chatroom import * 

collection_name = "chatroom"

router = APIRouter()

@router.get("/user", summary="특정 유저의 채팅방 정보를 조회합니다")
async def get_chatroom_one():
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        query = {"user": user}
        data = await mongodb.find_with_query(query)
        
        return ChatroomResponse(
            message=f"✅ Success Retrieve User Chat List: {len(data)}",
            data=data
        )
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Retrieve User Chat List: {e}")

@router.post("/", summary="채팅방을 생성합니다")
async def post_chatroom(data: ChatroomRequestData):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        insert_data = ChatroomData(
            **data.dict(),
            createDate=datetime.now()
        )
        mongodb.insert(insert_data.dict())
        return SuccessResponse(message=f"✅ Success Create Chatroom: {data['_id']}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Create Chatroomt: {e}")


@router.delete("/{id}", summary="특정 채팅방을 삭제합니다")
async def del_chatroom(id: str):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        await mongodb.delete(id)
        return SuccessResponse(message=f"✅ Success Delete Chatroom: {id}")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Retrieve User Chat List: {e}")