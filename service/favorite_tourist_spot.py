from sqlalchemy.orm import Session

from model.favorite_tourist_spot import FavoriteTouristSpot


class FavoriteTouristSpotService:

    def __init__(self, session: Session):
        self.session = session
    
    def insert(self, favorite: dict) -> FavoriteTouristSpot:
        favorite_loaded = FavoriteTouristSpot(**favorite)
        self.session.add(favorite_loaded)
        self.session.commit()
        self.session.refresh(favorite_loaded)
        return favorite_loaded

    def delete(self, favorite: FavoriteTouristSpot) -> None:
        self.session.delete(favorite)
        self.session.commit()