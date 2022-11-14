import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

from app.common.db import Base

author_has_languages = Table('author_has_languages', Base.metadata,
                             Column('author_id', Integer, ForeignKey('author.id')),
                             Column('language_id', Integer, ForeignKey('language.id'))
                             )


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birthday = Column(sqlalchemy.DATE, nullable=False)
    biography = Column(String(500), nullable=False)
    languages = relationship("Language", secondary=author_has_languages, backref="authors")

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)