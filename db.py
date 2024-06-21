import datetime

import dotenv
from dotenv import load_dotenv, dotenv_values
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, String, Date, ForeignKey, Integer, Time, LargeBinary
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

config = dotenv_values(".env")
engine = create_engine(
    "postgresql+psycopg2://Test2:cityofdreams5@localhost:5432/Kochevnik",
    echo=True
)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Status(Base):
    __tablename__ = "Status"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))


class Users(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    Surname: Mapped[str] = mapped_column(String(255))
    Name: Mapped[str] = mapped_column(String(255))
    Password: Mapped[str] = mapped_column(String(255))
    Email: Mapped[str] = mapped_column(String(255))
    Phone: Mapped[str] = mapped_column(String(255))
    fk_role: Mapped[int] = mapped_column(ForeignKey("Role.id"))
    Date_Birth: Mapped[datetime.date] = mapped_column(Date())

    def __repr__(self):
        return "<Users {}>".format(self.id)


class Dish(Base):
    __tablename__ = "Dish"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))
    Description: Mapped[str] = mapped_column(String(255))
    Price: Mapped[int] = mapped_column(Integer)
    Image: Mapped[str] = mapped_column(String(255), nullable=True)
    fk_Dish_Category: Mapped[int] = mapped_column(ForeignKey("Dish_Category.id"))


class Bron(Base):
    __tablename__ = "Bron"
    id: Mapped[int] = mapped_column(primary_key=True)
    Checkout_date: Mapped[str] = mapped_column(String(255))
    Checkin_date: Mapped[str] = mapped_column(String(255))
    fk_Room: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    fk_User: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    Price: Mapped[int] = mapped_column(Integer)
    Code: Mapped[str] = mapped_column(String(255))


class BlackList(Base):
    __tablename__ = "Black_List"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_User: Mapped[int] = mapped_column(ForeignKey("Users.id"))


class Order(Base):
    __tablename__ = "Order"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_User: Mapped[str] = mapped_column(ForeignKey("Users.id"))
    Price: Mapped[int] = mapped_column(Integer)
    Code: Mapped[str] = mapped_column(String(255))


class OrderStatus(Base):
    __tablename__ = "OrderStatus"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_Order: Mapped[int] = mapped_column(ForeignKey("Order.id"))
    fk_Status: Mapped[int] = mapped_column(ForeignKey("Status.id"))
    Time: Mapped[datetime.time] = mapped_column(Time)
    Date: Mapped[datetime.date] = mapped_column(Date())


class BronStatus(Base):
    __tablename__ = "BronStatus"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_Bron: Mapped[int] = mapped_column(ForeignKey("Bron.id"))
    fk_Status: Mapped[int] = mapped_column(ForeignKey("Status.id"))
    Time: Mapped[Time] = mapped_column(Time)
    Date: Mapped[datetime.date] = mapped_column(Date())


class DishCategory(Base):
    __tablename__ = "Dish_Category"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name_category: Mapped[str] = mapped_column(String(255))


class Rooms(Base):
    __tablename__ = "Rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))
    Number_seats: Mapped[int] = mapped_column(Integer)
    Price_Day: Mapped[int] = mapped_column(Integer)


class Role(Base):
    __tablename__ = "Role"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))


class OrderList(Base):
    __tablename__ = "Order_List"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_Order: Mapped[int] = mapped_column(ForeignKey("Order.id"))
    fk_Dish: Mapped[int] = mapped_column(ForeignKey("Dish.id"))
    Amount: Mapped[int] = mapped_column(Integer)
