from sqlalchemy.orm import Session

from model.tourist_spot import TouristSpot


class TouristSpotService:

    def __init__(self, session: Session):
        self.session = session
    
    def insert(self, tourist_spot: dict) -> TouristSpot:
        tourist_spot_loaded = TouristSpot(**tourist_spot)
        tourist_spot_loaded.category_id = tourist_spot['category']['id']
        del(tourist_spot_loaded.category)

        self.session.add(tourist_spot_loaded)
        self.session.commit()
        self.session.refresh(tourist_spot_loaded)
        return tourist_spot_loaded

    def get_by_name(self, name: str) -> TouristSpot:
        return self.session.query(
            TouristSpot
        ).filter(TouristSpot.name == name).first()