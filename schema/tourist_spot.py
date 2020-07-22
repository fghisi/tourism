from typing import List

from schema import BaseSchema
from schema.category import CategorySchema


class CategoryWithIdSchema(CategorySchema):
    id: int


class TouristSpotSchema(BaseSchema):
    name: str
    latitude: str
    longitude: str
    image: str 
    category: CategoryWithIdSchema


class TouristSpotWithIdSchema(TouristSpotSchema):
    id: int


class TouristSpotPagedSchema(BaseSchema):
    items: List[TouristSpotWithIdSchema]
    total: int


class FavoriteTouristSpotPagedSchema(BaseSchema):
    items: List[TouristSpotWithIdSchema]
    total: int