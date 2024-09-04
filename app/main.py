# > uvicorn app.main:app --host 0.0.0.0 --port 8502 --reload
import uvicorn 
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import logger
from app.core.config import configs
from app.api.v1.api import api_router
from app.database import mongodb 
from app.langchain.chatbot import chatbot
from app.schema.default import *

app = FastAPI(**configs.fastapi)
app.include_router(api_router)

# CORS 보안 처리
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 허용할 도메인 리스트
    allow_credentials=True,     # 자격증명 허용 여부
    allow_methods=["*"],        # 허용할 메서드 리스트 
    allow_headers=["*"]         # 허용할 HTTP 헤더
)

@app.on_event("startup")
async def startup_db_client():
    await mongodb.connect()

@app.get("/")
def root():
    return {"hello": "Python"}

@app.get("/reset")
def model_reset():
    chatbot.memory.chat_memory.clear()
    logger.info("✅ Reset Model")
    return SuccessResponse(message="✅ Reset Model")

from app.schema.chatting import ChatResponseData
from typing import List
from langchain.schema import HumanMessage, AIMessage

@app.post("/chat_history")
def model_history(chat_history: List[ChatResponseData]):
    try:
        for chat in chat_history:
            if chat.role == "user":
                chatbot.memory.chat_memory.add_user_message(chat.content)
            elif chat.role == "assistant":
                chatbot.memory.chat_memory.add_ai_message(chat.content)

        logger.info("✅ Insert Chat History into the Model")
        return SuccessResponse(message="✅ Insert Chat History into the Model")
    except Exception as e:
        return ErrorResponse(message=f"❌ Failed Insert Chat History into the Model: {e}")

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            receive_data = json.loads(data)
            
            response = ""
            async for token in chatbot.chain.astream(receive_data):
                response += token 
                # print(token, end="", flush=True)
                await websocket.send_text(token)
            await websocket.send_text("[EOS]")

            # 메모리 저장
            chatbot.save_memory(
                receive_data["request"],
                response
            )
    except:
        pass


