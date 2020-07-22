from typing import List
from sqlalchemy.orm import Session

from model.user import User
from model.tourist_spot import TouristSpot
from model.favorite_tourist_spot import FavoriteTouristSpot


class UserService:

    def __init__(self, session: Session):
        self.session = session
    
    def insert(self, user: dict) -> User:
        user_loaded = User(**user)
        self.session.add(user_loaded)
        self.session.commit()
        self.session.refresh(user_loaded)
        return user_loaded

    def get_by_email(self, email: str) -> User:
        return self.session.query(
            User
        ).filter(User.email == email).first()

    def get_favorite_tourist_spots(self,
        offset: int,
        limit: int,
        id: int
    ) -> List[TouristSpot]:
        return self.session.query(
            TouristSpot
        ).join(FavoriteTouristSpot.tourist_spots)\
            .filter(FavoriteTouristSpot.user_id == id)\
            .offset(offset).limit(limit).all()
