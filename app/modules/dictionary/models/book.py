from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from pydantic import BaseModel

from app.common.db import Base

book_has_authors = Table('book_has_authors', Base.metadata,
                         Column('book_id', Integer, ForeignKey('book.id')),
                         Column('author_id', Integer, ForeignKey('author.id'))
                         )


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    authors = relationship("Author", secondary=book_has_authors, backref="books")
    year = Column(Integer, nullable=False)
    language_id = Column(Integer, ForeignKey("language.id", ondelete="Cascade"))
    language = relationship("Language", lazy="selectin")
    is_readied = Column(BOOLEAN, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)

