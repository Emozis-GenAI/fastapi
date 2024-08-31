from fastapi import APIRouter, Body

from app.core.logger import logger
from app.database import mongodb 
from app.schema.default import *
from app.schema.user import *

from passlib.context import CryptContext 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

mongodb.set_collection("user")

router = APIRouter()

@router.post("/register", summary="회원가입")
async def register(user: RegisterData):
    # 비밀번호 해시
    user.hash_password()

    # ID 중복 확인 후 DB 삽입
    query = {"username": user.username}
    data = await mongodb.find_with_query(query)

    # ID 중복일 시
    if data:
        return ErrorResponse(message="❌ 이미 존재하는 ID입니다.")
    # UserData에 맞춰 DB 삽입
    else:
        try:
            insert_data = UserData(
                **user.dict(),
                createDate=datetime.now(),
                currentDate=None
            )
            print(insert_data)
            response = await mongodb.insert(insert_data.dict())
            return SuccessResponse(message=f"✅ Success Create User Data: {user.username}")
        except Exception as e:
            return ErrorResponse(message=f"❌ Failed Create User Data: {e}")


@router.post("/login", summary="로그인")
async def login(user: LoginData):
    # ID 조회
    query = {"username": user.username}
    data = await mongodb.find_with_query(query)

    # 아이디 존재
    if data:
        # 비밀번호 일치, 최근 접속 시간 변경
        if pwd_context.verify(user.password, data["password"]):
            new_data = {"currentDate": datetime.now()}
            await mongodb.update(data["_id"], new_data)
            return UserResponse(
                message=f"✅ Success Login",
                data=UserResponseData(
                    username=data["username"], 
                    nickname=data["nickname"]
                )
            )
        # 비밀번호 불일치
        else:
            return ErrorResponse(message="❌ 비밀번호가 일치하지 않습니다")
    # 아이디 조회 안됨
    else:
        return ErrorResponse(message="❌ 아이디가 존재하지 않습니다")


    
    

    
    