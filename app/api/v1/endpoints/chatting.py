from fastapi import APIRouter, Body

from app.database import mongodb
from app.schema.chatting import *

collection_name = "chatting"

router = APIRouter()

@router.get("/{chatroom_id}", summary="특정 채팅방 대화 히스토리를 조회합니다")
async def get_chat_history(chatroom_id: str):
    # Collection 연결
    await mongodb.get_collection(collection_name)

    try:
        query = {"chatroom_id": chatroom_id}
        data = await mongodb.find_with_query(query)
        
        return ChatHistoryResponse(
            message=f"✅ Success Retrieve Chat History: {len(data)}",
            data=data
        )
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Retrieve Chat History: {e}")

@router.post("/", summary="채팅을 DB에 저장합니다")
async def post_chat_history(data: ChatRequestData):
    # Collection 연결
    await mongodb.get_collection(collection_name)
    
    try:
        insert_data = ChatData(
            **data.dict(),
            createDate=datetime.now()
        )
        await mongodb.insert(insert_data.dict())
        return SuccessResponse(message=f"✅ Success Save Chat History")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Save Chat History: {e}")
