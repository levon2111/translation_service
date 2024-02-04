from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from app.common import messages
from app.common.response import Response
from app.common.translate import translate_text
from app.database.db import get_db
from app.models.models import Translation, WordInDB
from app.schemas.schemas import create_word, delete_word, get_word, get_words

router = APIRouter()


@router.get("/", include_in_schema=False, status_code=200)
@router.get("", response_model=WordInDB, status_code=200, responses={400: {}})
async def get_word_details(
    word: str,
    target_language_code: str,
    db: AsyncIOMotorClient = Depends(get_db),
    source_language_code: str = None,
):
    db_word = await get_word(db, word)
    if db_word:
        return db_word
    else:
        translation = await translate_text(
            word,
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )
        options = [
            Translation(language=target_language_code, translation=i.translated_text)
            for i in translation.translations
        ]
        word = await create_word(db, word=word, translations=options)

        data = jsonable_encoder(word)

        return Response(data, message=messages.SUCCESS, code=status.HTTP_200_OK)


@router.delete("/{word}", status_code=204)
async def delete_word_route(word: str, db: AsyncIOMotorClient = Depends(get_db)):
    deleted = await delete_word(db, word)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Word '{word}' not found")
    return {"message": f"Word '{word}' successfully deleted"}


@router.get("/list", response_model=List[WordInDB])
async def word_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    conn: AsyncIOMotorClient = Depends(get_db),
):
    words = await get_words(conn, skip=skip, limit=limit)
    return words
