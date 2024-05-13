from flask_login import UserMixin

from db import Session, Users
from sqlalchemy import select


class UserLogin():
    def from_DB(self, user_id):
        with Session() as session:
            statement = select(Users).where(Users.id == str(user_id))
            return session.execute(statement).fetchone()[0]

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)