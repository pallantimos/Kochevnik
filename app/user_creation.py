import datetime
import re
from pydantic import BaseModel, field_validator, ValidationError
from db import Users
from sqlalchemy import select
from db import Session


class UserCreationSchema(BaseModel):
    surname: str
    name: str
    password: str
    email: str
    phone: str
    date: str

    @field_validator("password")
    @classmethod
    def password_now(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Пароль должен быть длинее 8 символов")
        if not any(c.isupper() for c in value):
            raise ValueError("Пароль должен содержать заглавные буквы")
        if not any(c.islower() for c in value):
            raise ValueError("Пароль должен содержать строчные буквы")
        if not any(c.isdigit() for c in value):
            raise ValueError("Пароль должен содержать цифру")
        if not re.match("[a-zA-Z0-9]+$", value):
            raise ValueError(
                "Пароль должен содержать только английские буквы и цифры"
            )
        return value

    @field_validator("date")
    @classmethod
    def date_now(cls, value: str) -> str:
        if int(value[:4]) >= datetime.date.today().year:
            raise ValueError(
                "Некорректная дата рождения"
            )
        if int(value[:4]) < datetime.date.today().year - 200:
            raise ValueError(
                "Некорректная дата рождения"
            )
        return value
    @field_validator("phone")
    @classmethod
    def date_now(cls, value: str) -> str:
        with Session() as session:
            statement = select(Users).where(Users.Phone == value)
            result = session.execute(statement).scalar()
            if result:
                raise ValueError(
                    "Телефон зарегистрирован"
                )
        return value
    @field_validator("email")
    @classmethod
    def date_now(cls, value: str) -> str:
        with Session() as session:
            statement = select(Users).where(Users.Email == value)
            result = session.execute(statement).scalar()
            if result:
                raise ValueError(
                    "Почта зарегистрирована"
                )
        return value
    @field_validator("email")
    @classmethod
    def email_now(cls, value: str) -> str:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Неправильный формат почты")
        return value
