from schema import BaseSchema


class UserSchema(BaseSchema):
    email: str
    password: str