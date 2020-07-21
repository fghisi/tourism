from sqlalchemy import Column, Integer, String

from model import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)