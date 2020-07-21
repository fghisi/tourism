from sqlalchemy.orm import Session

from model.user import User


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