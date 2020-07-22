from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class TouristSpot(Base):
    __tablename__ = "tourist_spot"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    image = Column(String)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', uselist=False)