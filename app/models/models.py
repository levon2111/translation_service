from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.mongo_model import MongoModel


class Translation(BaseModel):
    language: str = Field(..., example="es")
    translation: str = Field(..., example="desafío")


class WordDefinition(BaseModel):
    definitions: List[str] = Field(default=[],
                                   example=["A contest or competition.", "A call or summons to engage in any contest."])
    synonyms: List[str] = Field(default=[], example=["contest", "competition"])
    translations: List[Translation] = Field(default=[], example=[{"language": "es", "translation": "desafío"}])
    examples: List[str] = Field(default=[], example=["The team faced a tough challenge."])


class Word(BaseModel):
    word: str = Field(..., example="challenge")
    details: Optional[WordDefinition] = None


class WordInDB(Word, MongoModel):
    id: str = Field(..., example="507f191e810c19729de860ea")


class WordCreate(Word):
    pass


class WordUpdate(BaseModel):
    details: Optional[WordDefinition] = None
