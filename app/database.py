import os 
import asyncio
from datetime import datetime
from dotenv import load_dotenv 
from motor.motor_asyncio import AsyncIOMotorClient 
from pymongo.server_api import ServerApi 
from bson.objectid import ObjectId

from app.core.config import configs 
from app.core.logger import logger 

load_dotenv()
const = configs.mongodb 
username = os.getenv(const["userKey"])
password = os.getenv(const["pwdKey"])
host = const["host"]
db_name = const["database"]

class MongoDB:
    def __init__(self):
        self.uri = f"mongodb+srv://{username}:{password}@{host}"
        self.client = AsyncIOMotorClient(self.uri, server_api=ServerApi("1"))
        self.db = self.client.get_database(db_name)
        self.collection_name = None
    
    # DB 연결
    async def connect(self):
        try:
            await self.client.server_info()
            logger.info("✅ Success Connect MongoDB Client")

            db_list = await self.client.list_database_names()
            if db_name in db_list:
                self.db = self.client.get_database(db_name)
                logger.info(f"✅ Success Get Database: {db_name}")
            else:
                logger.warning(f"{db_name} is not in database list")
        except Exception as e:
            logger.warning(f"❌ Connect Failed Client: {e}")

    # Collection CRD
    async def manage_collection(self, collection_name=None, method="get"):
        collection_list = await self.db.list_collection_names()
        if method == "get":
            return collection_list
        if method == "create":
            if collection_name not in collection_list:
                try:
                    await self.db.create_collection(collection_name)
                    message = f"🪄 Create Collection: {collection_name}"
                    logger.info(message)
                except Exception as e:
                    message = f"Failed Create Collection: {e}"
                    logger.warning(message)
            else:
                message = f"❌ 이미 존재하는 Collection 입니다."
                logger.warning(message)
        elif method == "drop":
            if collection_name in collection_list:
                try:
                    await self.db.drop_collection(collection_name)
                    message = f"🗑️ Drop Collection: {collection_name}"
                    logger.info(message)
                except Exception as e:
                    message = f"Failed Drop Collection: {e}"
                    logger.info(message)
            else:
                message = f"❌ Collection이 존재하지 않습니다."
                logger.warning(f"❌ Collection이 존재하지 않습니다.")

        return message
    
    # Collection 이름 설정
    def set_collection(self, collection_name):
        self.collection_name = collection_name
    
    # Collection 연결
    async def _get_collection(self, collection_name):
        collection_list = await self.db.list_collection_names()
        if collection_name in collection_list:
            self.collection = self.db.get_collection(collection_name)
            logger.info(f"Success Get Collection: {collection_name}")
        else:
            logger.warning(f"{collection_name} is not in collection list")

    # 모든 정보 조회
    async def find_all(self):
        await self._get_collection(self.collection_name)

        data = []
        async for element in self.collection.find():
            element["_id"] = str(element["_id"])
            data.append(element)
        logger.info(f"🔍 RETRIEVE SUCCESS: {len(data)}")
        return data  
    
    # _id로 조회
    async def find_one(self, id):
        await self._get_collection(self.collection_name)

        try:
            query = {"_id": ObjectId(id)}
            data = await self.collection.find_one(query)
            data["_id"] = str(data["_id"])
            logger.info(f"🔍 RETRIEVE SUCCESS: {data}")
            return data  
        except Exception as e:
            logger.warning(f"RETRIEVE ERROR: {e}")
    
    # 쿼리로 조회
    async def find_with_query(self, query):
        await self._get_collection(self.collection_name)

        try:
            data = []
            async for element in self.collection.find(query):
                element["_id"] = str(element["_id"])
                data.append(element)
            logger.info(f"🔍 RETRIEVE SUCCESS: {len(data)}")

            if len(data) == 1:
                return data[0]
            return data  
        except Exception as e:
            logger.warning(f"RETRIEVE ERROR: {e}")

    # 삽입
    async def insert(self, data):
        await self._get_collection(self.collection_name)

        if isinstance(data, dict):
            data = [data]
        
        try:
            response = []
            for element in data:
                res = await self.collection.insert_one(element)
                response.append(str(res.inserted_id))
            logger.info(f"➕ INSERT SUCCESS: {response}")
            return response
        except Exception as e:
            logger.warning(f"INSERT ERROR: {e}")

    # 업데이트
    async def update(self, id, new_data):
        await self._get_collection(self.collection_name)

        try:
            query = {"_id": ObjectId(id)}
            await self.collection.update_one(query, {"$set": new_data})
            logger.info(f"⚙️ Update SUCCESS: {id}")
        except Exception as e:
            logger.warning(f"RETRIEVE ERROR: {e}")

    # 삭제
    async def delete(self, id):
        await self._get_collection(self.collection_name)

        try:
            query = {"_id": ObjectId(id)}
            await self.collection.delete_one(query)
            logger.info(f"🗑 DELETE SUCCESS: {id}")
        except Exception as e:
            logger.warning(f"DELETE ERROR: {e}")

mongodb = MongoDB()
