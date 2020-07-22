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

    def get(self, offset: int, limit: int, name: str):
        query = self.session.query(
            TouristSpot
        )
        
        if name:
            query = query.filter(TouristSpot.name == name)
        
        return query.offset(offset).limit(limit).all()

    def get_by_name(self, name: str) -> TouristSpot:
        return self.session.query(
            TouristSpot
        ).filter(TouristSpot.name == name).first()

    def get_by_id(self, id: int) -> TouristSpot:
        return self.session.query(
            TouristSpot
        ).filter_by(id=id).one()