import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from app.common.util import uuid_masker
from app.conf.config import Config
from app.models.models import Translation, WordDefinition, WordInDB

__db_name = Config.app_settings.get("db_name")
__db_collection = "word"


async def create_word(
    conn: AsyncIOMotorClient, word: str, translations: List[Translation]
) -> WordInDB:
    new_word = WordInDB(
        id=str(uuid4()),
        word=word,
        details=WordDefinition(translations=translations),
        create_time=datetime.utcnow(),
        update_time=datetime.utcnow(),
        deleted=False,
    )
    logging.info(f"Inserting `{word}` word into db.")
    await conn[__db_name][__db_collection].insert_one(new_word.mongo())
    logging.info(f"word {word} has inserted into db")
    return new_word


async def get_word(conn: AsyncIOMotorClient, word_str: str) -> Optional[WordInDB]:
    logging.info(f"Getting word {word_str}...")
    word = await conn[__db_name][__db_collection].find_one(
        {
            "$and": [
                {"word": word_str},
            ]
        },
    )
    if None is word:
        logging.info(f"The word {word_str} not found in db.")
    else:
        word["id"] = word["_id"]
        word = WordInDB.parse_obj(word)
    return word


async def update_word(
    conn: AsyncIOMotorClient, resource_id: UUID, resource_data: dict
) -> Optional[WordInDB]:
    logging.info(f"Updating word {uuid_masker(str(resource_id))}...")
    word = await conn[__db_name][__db_collection].find_one_and_update(
        {
            "$and": [
                {"_id": resource_id},
            ]
        },
        {
            "$set": {
                **resource_data,
                "update_time": datetime.utcnow(),
            }
        },
        return_document=ReturnDocument.AFTER,
    )
    if None is word:
        logging.error(f"Word {uuid_masker(str(resource_id))} not exist")
    else:
        logging.info(f"Word {uuid_masker(str(resource_id))} updated")
    word["id"] = word["_id"]

    return WordInDB.parse_obj(word)


async def delete_word(
    conn: AsyncIOMotorClient,
    word: str,
) -> Optional[WordInDB]:
    logging.info(f"Deleting word `{word}`.")

    word = await conn[__db_name][__db_collection].find_one_and_delete({"word": word})

    if None is word:
        logging.error(f"word {word} not exist")
    else:
        logging.info(f"word {word} deleted")
    return word


async def get_words(conn: AsyncIOMotorClient, skip: int, limit: int) -> List[WordInDB]:
    cursor = conn[__db_name][__db_collection].find().skip(skip).limit(limit)
    words = await cursor.to_list(length=limit)
    for word in words:
        word["id"] = word["_id"]
    return words
