from sqlalchemy import Column, String, Text
from utils.db.database import Base


class Button(Base):
    __tablename__ = 'buttons'
    id = Column(String(255), unique=True, primary_key=True)
    name = Column(String(255))
    url = Column(Text())

    def __init__(self, id=None, name=None, url=None):
        self.id = id
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Button %r>' % (self.name)
