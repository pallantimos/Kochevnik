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


class ShoppingCart(Base):
    __tablename__ = "ShoppingCart"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_User: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    Price: Mapped[int] = mapped_column(Integer())


class ShoppingCartList(Base):
    __tablename__ = "ShoppingCartList"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_ShoppingCart: Mapped[int] = mapped_column(ForeignKey("ShoppingCart.id"))
    fk_Dish: Mapped[int] = mapped_column(ForeignKey("Dish.id"))
    Amount: Mapped[int] = mapped_column(Integer())


class Dish(Base):
    __tablename__ = "Dish"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))
    Description: Mapped[str] = mapped_column(String(255))
    Price: Mapped[int] = mapped_column(Integer)
    fk_Dish_Category: Mapped[int] = mapped_column(ForeignKey("Dish_Category.id"))


class Bron(Base):
    __tablename__ = "Bron"
    id: Mapped[int] = mapped_column(primary_key=True)
    Date: Mapped[str] = mapped_column(String(255))
    fk_Room: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    fk_User: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    Amount_day: Mapped[int] = mapped_column(Integer)
    Time: Mapped[Time] = mapped_column(Time)
    Price: Mapped[int] = mapped_column(Integer)


class Order(Base):
    __tablename__ = "Order"
    id: Mapped[int] = mapped_column(primary_key=True)
    Date: Mapped[datetime.date] = mapped_column(Date())
    fk_User: Mapped[str] = mapped_column(ForeignKey("Users.id"))
    Price: Mapped[int] = mapped_column(Integer)
    Code: Mapped[str] = mapped_column(String(255))


class ChangesStatusOrder(Base):
    __tablename__ = "Changes_Status_Order"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_Order: Mapped[int] = mapped_column(ForeignKey("Order.id"))
    fk_Status: Mapped[int] = mapped_column(ForeignKey("Order_Status.id"))
    Time: Mapped[Time] = mapped_column(Time)
    Date: Mapped[datetime.date] = mapped_column(Date())


class ChangesStatusBron(Base):
    __tablename__ = "Changes_Status_Bron"
    id: Mapped[int] = mapped_column(primary_key=True)
    fk_Order: Mapped[int] = mapped_column(ForeignKey("Bron.id"))
    fk_Status: Mapped[int] = mapped_column(ForeignKey("Bron_Status.id"))
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


class BronStatus(Base):
    __tablename__ = "Bron_Status"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))


class OrderStatus(Base):
    __tablename__ = "Order_Status"
    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(255))
