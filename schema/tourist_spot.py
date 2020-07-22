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