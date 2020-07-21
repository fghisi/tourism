from schema import BaseSchema


class User(BaseSchema):
    email: str
    password: str