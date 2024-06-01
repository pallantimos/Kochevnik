from flask_login import UserMixin

from db import Session, Users
from sqlalchemy import select


class UserLogin():
    def get_current_user_info(self):
        user = {
            "Name": self.__user.Name,
            "Email": self.__user.Email,
            "Password": self.__user.Password,
            "Surname": self.__user.Surname,
            "Phone": self.__user.Phone,
        }
        return user

    def from_DB(self, user_id):
        with Session() as session:
            statement = select(Users).where(Users.id == user_id)
            self.__user = session.execute(statement).fetchone()[0]
            return self

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