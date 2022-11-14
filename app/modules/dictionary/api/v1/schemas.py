import datetime
from typing import List

import sqlalchemy
from pydantic import BaseModel

from app.modules.dictionary.models import Author, Book, Language


class AuthorBase(BaseModel):
    id: int
    name: str
    birthday: datetime.date
    biography: str

    class Config:
        orm_mode = True


class LanguageBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    id: int
    name: str
    year: int
    is_readied: bool

    class Config:
        orm_mode = True


class BookSchema(BookBase):
    authors: List[AuthorBase]
    language: LanguageBase


class AuthorSchema(AuthorBase):
    languages: List[LanguageBase]
