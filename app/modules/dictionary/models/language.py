from sqlalchemy import Column, Integer, String

from app.common.db import Base

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Language, self).__init__(*args, **kwargs)