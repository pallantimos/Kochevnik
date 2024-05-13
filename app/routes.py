import datetime
from dotenv import dotenv_values
from flask import render_template, request, abort, make_response, flash, session
from flask_login import login_manager, LoginManager, login_user, login_required, current_user
from sqlalchemy import insert, select, delete, text
from app import app
from app.user_creation import UserCreationSchema
from db import Users, Session, Role, Order, OrderList, OrderStatus, BronStatus, ChangesStatusOrder, ShoppingCart, ShoppingCartList
from flask_recaptcha import ReCaptcha
from pydantic import ValidationError
import hashlib
import config


from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager(app)


class UserLogin():
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


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().from_DB(user_id)


@app.route("/")
@app.route("/index")
def index():
    if 'visits' in session:
        session['visits'] = session['visits'] + 1
    else:
        session['visits'] = 1
    return render_template("index2.html", visits=session['visits'])


@app.route('/loginsubmit', methods=["POST", "GET"])
def login_submit():
    phone = request.json["tel"]
    password = request.json["password"]
    with Session() as sessionn:
        statement = select(Users).where(
            Users.Phone == phone,
        )
        result = sessionn.execute(statement)
        result = result.fetchone()

        encoding_password = password.encode('utf-8')
        hashed_password = hashlib.md5(encoding_password.strip()).hexdigest()

        if result and str(hashed_password) == result[0].Password:
            print("Login Successful")
            response = make_response(jsonify({"success": True}), 200)
            response.headers["Location"] = url_for("index")
            user_login = UserLogin().create(result[0])
            login_user(user_login)
            return response
        elif not result:
            flash("Пользователь не найден", "danger")
            response = make_response(jsonify({"error": "Пользователь не найден"}), 401)
            response.headers["Location"] = url_for("login")
            return response
        elif str(hashed_password) != result.Password:
            flash("Неправильный пароль", "danger")
            response = make_response(jsonify({"error": "Неправильный пароль"}), 401)
            response.headers["Location"] = url_for("login")
            return response


@app.route("/registratesubmit", methods=["POST"])
def registration_submit():
    try:
        user = UserCreationSchema.model_validate(request.json)
        print(user.model_dump())
        hashed_password = str(hashlib.md5(request.json['password'].encode()).hexdigest())
        user = Users(
            Surname=request.json["surname"],
            Name=request.json["name"],
            Password=hashed_password,
            Email=request.json["email"],
            Phone=request.json["phone"],
            Date_Birth=request.json["date"],
            fk_role=1
        )

        with Session() as session:
            session.add(user)
            session.flush()
            session.commit()
            statement = select(Users).order_by(Users.id.desc())
            result = session.execute(statement)
            result = result.scalar()
            shopping_cart = ShoppingCart(
                fk_User=result.id,
                Price=0,
            )
            session.add(shopping_cart)
            session.flush()
            session.commit()

    except (ValidationError, Exception) as er:
        # return jsonify(er.args[0]), 400
        # app.logger.error(er.args[0])
        response = make_response(jsonify({"error": repr(er.errors()[0]['msg'])}), 401)
        return response

    return render_template("index2.html")


@app.route("/registrate")
@login_required
def registration():
    return render_template("registr.html")


@app.route("/login")
def login():
    if 'visits' in session:
        session['visits'] = session['visits'] + 1
    else:
        session['visits'] = 1
    return render_template("login.html", visits=session['visits'])


@app.route("/order")
def order():

    return render_template("order.html")


@app.route("/hotels")
def hotels():
    return render_template("hotels.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/basket")
def basket():
    return render_template("basket.html")

# TODO
#
# @app.route("/shoppingcartadd", methods=["POST"])
# def shopping_cart_add():
#     with Session() as session:
#         statement = select(ShoppingCart.id).where(ShoppingCart.fk_User == request.json["fk_User"])
#         result = session.execute(statement)
#         result = result.scalar()
#         dish = ShoppingCartList(
#
#             fk_Dish=request.json["dish"],
#             fk_ShoppingCart=select(ShoppingCart.id).where(ShoppingCart.fk_User == select(Users.id).where(Users.)),
#         )
#         session.add(order)
#
#         session.add(OrderList(
#             fk_Order=order.id,
#             Amount=request.json["amount"],
#             fk_Dish=request.json["dish"],
#         ))
#         session.flush()
#         session.commit()


@app.route("/ordersubmit", methods=["POST"])
def order_submit():
    with Session() as session:
        order = Order(
            Date=datetime.date.today(),
            Price=int(request.json["price"]),
            Code=config.random_string(),
            fk_User=request.json['user']
        )
        session.add(order)

        session.add(OrderList(
            fk_Order=order.id,
            Amount=request.json["amount"],
            fk_Dish=request.json["dish"],
        ))
        session.flush()
        session.commit()

# TODO


@app.route("/orderadminsubmit", methods=["POST"])
def order_admin_submit():
    with Session() as session:
        statement = select(Order).where(
            Order.Code == request.json["code"],
        )
        result = session.execute(statement)
        result = result.scalar()
        statement = select(ChangesStatusOrder).where(
            ChangesStatusOrder.fk_Order == result.id,
        )

        result = session.execute(statement)
        result.scalar()
        result.fk_Status = 2
        session.flush()
        session.commit()


@app.route("/orderadminsubmitready", methods=["POST"])
def order_admin_submit_ready():
    with Session() as session:
        statement = select(Order).where(
            Order.Code == request.json["code"],
        )
        result = session.execute(statement)
        result = result.scalar()
        statement = select(ChangesStatusOrder).where(
            ChangesStatusOrder.fk_Order == result.id,
        )

        result = session.execute(statement)
        result.scalar()
        result.fk_Status = 3
        session.flush()
        session.commit()
