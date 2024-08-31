# > uvicorn app.main:app --host 0.0.0.0 --port 8502 --reload
import uvicorn 
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import configs
from app.api.v1.api import api_router
from app.database import mongodb 

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

@app.post("/chat", summary="AI 답변을 생성합니다")
def chat():
    return {"hello": "Python"}
