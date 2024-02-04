import json
import logging
import os
from datetime import datetime
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient


class MongoHandler():
    def __init__(self, db_name: str, collection_name: str):
        self.__db_name = db_name
        self.__collection_name = collection_name
        self.__db_client = AsyncIOMotorClient(
            os.environ.get('MONGO_DB_TEST')
        )

    async def get_word(self, name: str):
        return await self.__db_client[self.__db_name][self.__collection_name] \
            .find_one({'name': name})

    async def insert_word(self, word: dict):
        await self.__db_client[self.__db_name][self.__collection_name] \
            .insert_one(word)

    async def drop_database(self):
        await self.__db_client.drop_database(self.__db_name)

    def close_conn(self):
        self.__db_client.close()


class MongoClient():
    def __init__(self, db_name: str, collection_name: str):
        self.__db_handler = MongoHandler(db_name, collection_name)

    async def __aenter__(self):
        await self.__create_mock_data()
        return self.__db_handler

    async def __create_mock_data(self):
        with open('tests/mock_data/word.json', 'r') as f:
            word_json = json.load(f)
            for word in word_json:
                word['create_time'] = datetime.strptime(
                    word['create_time'], '%Y-%m-%d %H:%M:%S'
                )
                word['update_time'] = datetime.strptime(
                    word['update_time'], '%Y-%m-%d %H:%M:%S'
                )
                word['_id'] = UUID(word['_id'])
                await self.__db_handler.insert_word(word)

    async def __aexit__(
            self, exception_type,
            exception_value, exception_traceback
    ):
        if exception_type:
            logging.error(exception_value)

        await self.__db_handler.drop_database()
        self.__db_handler.close_conn()
        return False
