import jwt
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from datetime import datetime, timedelta

from model.user import User


class JWT:

    def get(self, payload: dict) -> str:
        payload['exp'] = self._get_exp()
        return jwt.encode(
            payload, 
            'secret', 
            algorithm='HS256'
        ).decode('utf-8')
        
    def validate(self, jwtcd):
        try:
            return jwt.decode(jwtcd, 'secret')
        except ExpiredSignatureError:
            raise JWTExceptionExpired
        
    def _get_exp(self):
        return datetime.utcnow() + timedelta(hours=1)


class AuthenticationService:

    def __init__(self, session: Session):
        self.session = session

    def _validate(self, email: str, password: str) -> bool:
        user = self.session.query(
            User
        ).filter(User.email == email)\
        .filter(User.password == password).all()

        if not user:
            raise EmailOrPasswordInvalid

        return True

    def get_token(self, email: str, password: str) -> JWT:
        if self._validate(email, password):
            return JWT().get(
                {'email': email}
            )


class EmailOrPasswordInvalid(Exception):
    pass


class JWTExceptionExpired(Exception):
	pass