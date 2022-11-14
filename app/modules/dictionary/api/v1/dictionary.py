import datetime
from typing import Union, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import not_
from sqlalchemy.orm import Session

from app.modules.dictionary.models import Author, Book, Language
from app.modules.dictionary.api.v1.schemas import AuthorSchema, BookSchema
from app.common.db import get_db

router = APIRouter()


@router.get("/")
def read_root(session: Session = Depends(get_db)):
    try:
        return [
            {
                "unread books": [
                    {
                        "name": x.name,
                        "year": x.year,
                        "language": x.language.name,
                        "authors": [
                            {
                                "name": y.name
                            } for y in x.authors
                        ]
                    } for x in session.query(Book).filter(Book.is_readied == "false").all()
                ],
                "readied books":
                    [
                        {
                            "name": x.name,
                            "year": x.year,
                            "language": x.language.name,
                            "authors": [
                                {
                                    "name": y.name
                                } for y in x.authors
                            ]
                        } for x in session.query(Book).filter(Book.is_readied == "true").all()
                    ]
            }
        ]
    except:
        return {"status": "no data to return"}


@router.post("/language/")
def post_language(lang: str, session: Session = Depends(get_db)):
    new_lang = Language(name=lang)
    session.add(new_lang)
    session.commit()

    return {"status": "success"}


@router.post("/books", response_model=List[BookSchema])
def post_book(name: str, year: int, lang: str, is_readied: bool, authors: list[str] = Query(),
              session: Session = Depends(get_db)):
    new_book = Book(name=name, year=year, is_readied=is_readied)
    new_book.language = session.query(Language).filter(Language.name == lang).one()
    new_authors = []
    for author in authors:
        new_authors.append(session.query(Author).filter(Author.name == author).one())
    new_book.authors = new_authors
    session.add(new_book)
    session.commit()

    return new_book


@router.post("/authors", response_model=List[AuthorSchema])
def post_author(name: str, birthday: datetime.date, biography: str, languages: list[str] = Query(),
                session: Session = Depends(get_db)):
    new_author = Author(name=name, birthday=birthday, biography=biography)
    new_languages = []
    for language in languages:
        new_languages.append(session.query(Language).filter(Language.name == language).one())
    new_author.languages = new_languages
    session.add(new_author)
    session.commit()

    return new_author


@router.put("/book{id}", response_model=List[BookSchema])
def put_book(book_id: int, name: Union[str, None] = None, lang: Union[str, None] = None, year: Union[int, None] = None,
             authors: list[str] = Query(None), is_readied: Union[bool, None] = None,
             session: Session = Depends(get_db)):
    book = session.query(Book).filter(Book.id == book_id).one()
    if name is not None:
        book.name = name

    if lang is not None:
        book.language = session.query(Language).filter(Language.name == lang).one()

    if year is not None:
        book.year = year

    if authors is not None:
        new_authors = []
        for author in authors:
            new_authors.append(session.query(Author).filter(Author.name == author).one())
        book.authors = new_authors

    if is_readied is not None:
        book.is_readied = is_readied

    session.commit()

    return book


@router.put("/authors{id}", response_model=List[AuthorSchema])
def put_author(author_id: int, name: Union[str, None] = None, birthday: Union[datetime.date, None] = None,
               biography: Union[str, None] = None, languages: list[str] = Query(None),
               session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == author_id).one()

    if name is not None:
        author.name = name
    #
    if birthday is not None:
        author.birthday = birthday

    if biography is not None:
        author.biography = biography

    if languages is not None:
        new_languages = []
        for language in languages:
            new_languages.append(session.query(Language).filter(Language.name == language).one())
        author.languages = new_languages

    session.commit()

    return author


@router.delete("/books/{id}")
def delete_book(book_id: int, session: Session = Depends(get_db)):
    try:
        book = session.query(Book).filter(Book.id == book_id).one()
        session.delete(book)
        session.commit()

        return {"status": "success"}
    except:
        return {"status": "bad"}


@router.delete("/authors/{id}")
def delete_author(author_id: int, session: Session = Depends(get_db)):
    try:
        author = session.query(Author).filter(Author.id == author_id).one()
        session.delete(author)
        session.commit()
        return {"status": "success"}
    except:
        return {"status": "bad"}


@router.get("/books/author/", response_model=List[BookSchema])
def get_author_books(author_name: str, lang: Union[str, None] = None, is_readied: Union[bool, None] = None,
                     session: Session = Depends(get_db)):
    try:
        author = session.query(Author).filter(Author.name == author_name).one()
        books = session.query(Book).filter(Book.authors.contains(author)).all()
    except:
        books = []
        return books

    if lang is not None and is_readied is None:
        try:
            print(1)
            lang_id = session.query(Language).filter(Language.name == lang).one()
            books = session.query(Book).filter(Book.language_id == lang_id.id, Book.authors.contains(author)).all()
        except:
            books = []
            return books

    if is_readied is not None and lang is None:
        try:
            print(2)
            books = session.query(Book).filter(Book.is_readied == is_readied, Book.authors.contains(author)).all()
        except:
            books = []
            return books

    if lang is not None and is_readied is not None:
        try:
            print(3)
            lang_id = session.query(Language).filter(Language.name == lang).one()
            books = session.query(Book).filter(Book.language_id == lang_id.id, Book.is_readied == is_readied,
                                                    Book.authors.contains(author)).all()
        except:
            books = []
            return books

    return books


@router.get("/books/readied", response_model=List[BookSchema])
def get_readied_books(session: Session = Depends(get_db)):
    books = session.query(Book).filter(Book.is_readied).all()

    return books


@router.get("/books/unread", response_model=List[BookSchema])
def get_unread_books(lang: Union[str, None] = None, session: Session = Depends(get_db)):
    books = []
    if lang is None:
        books = session.query(Book).filter(not_(Book.is_readied)).all()
    else:
        try:
            lang_id = session.query(Language).filter(Language.name == lang).one()
            books = session.query(Book).filter(not_(Book.is_readied), Book.language_id == lang_id.id).all()
        except:
            books = []

    return books


@router.get("/books", response_model=List[BookSchema])
def get_book_by_name(book_name: str, session: Session = Depends(get_db)):
    books = session.query(Book).filter(Book.name == book_name).all()

    return books


@router.get("/authors", response_model=List[AuthorSchema])
def get_author_by_name(author_name: str, session: Session = Depends(get_db)):
    authors = session.query(Author).filter(Author.name == author_name).all()

    return authors
