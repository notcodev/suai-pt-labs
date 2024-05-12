from sqlalchemy.orm.session import Session

from src.schema import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, username, email, password):
        user = User(username=username, email=email, password=password)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
