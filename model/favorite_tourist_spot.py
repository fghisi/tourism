from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class FavoriteTouristSpot(Base):
    __tablename__ = "favorite_tourist_spot"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    tourist_spot_id = Column(Integer, ForeignKey('tourist_spot.id'))
    tourist_spots = relationship('TouristSpot', uselist=True)