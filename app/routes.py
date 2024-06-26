import datetime
from dotenv import dotenv_values
from flask import render_template, request, abort, make_response, flash, session, get_flashed_messages
from flask_login import login_manager, LoginManager, login_user, login_required, current_user, logout_user
from sqlalchemy import insert, select, delete, text, update, join
from app import app
from app.UserLogin import UserLogin
from app.user_creation import UserCreationSchema
from db import Users, Session, Role, Order, OrderList, OrderStatus, BronStatus, Dish, Rooms, Bron, Status, BlackList
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

bp = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для заказа и бронирования"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().from_DB(user_id)


@app.route("/registratesubmit", methods=["POST", "GET"])
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
            order = Order(
                fk_User=result.id,
                Price=0,
                Code=config.random_string(),
            )
            session.add(order)
            session.flush()
            session.commit()

            statement = select(Order).order_by(Order.id.desc())
            result = session.execute(statement)
            result = result.scalar()
            status = OrderStatus(
                fk_Order=result.id,
                fk_Status=1,
                Time=datetime.datetime.now().time(),
                Date=datetime.datetime.now().date(),
            )
            session.add(status)
            session.flush()
            session.commit()

    except (ValidationError, Exception) as er:
        # return jsonify(er.args[0]), 400
        # app.logger.error(er.args[0])
        response = make_response(jsonify({"error": repr(er.errors()[0]['msg'])}), 401)
        return response

    return render_template("index2.html")


@app.route("/registrate")
def registration():
    return render_template("registr.html")


@app.route("/adminprofile")
def admin_profile():
    admin = current_user.get_current_user_info()
    return render_template("adminprofile.html", admin=admin)


@app.route("/adminorder", methods=["POST", "GET"])
def admin_order():
    with Session() as session:
        orders_answer = []
        if request.method == "POST":
            with Session() as session:
                session.execute(
                    update(OrderStatus)
                    .where(OrderStatus.fk_Order == request.json['orderId'])
                    .values(fk_Status=int(request.json['statusId']) + 1)
                )
                session.flush()
                session.commit()
            return make_response(jsonify({"success": "true"}), 200)

        if request.method == "GET":
            orders = session.query(Order).order_by(Order.id.desc())
            orders_statuses = session.execute(select(Status.Name).join(OrderStatus).where(Status.id == OrderStatus.fk_Status).order_by(OrderStatus.fk_Order.desc()))
            orders_statuses = orders_statuses.fetchall()
            orders_statuses = [str(el)[2:-3] for el in orders_statuses]
            for i in range(len(orders_statuses)):
                item = {'id': orders[i].id, 'Price': orders[i].Price, "Code": orders[i].Code, "fk_User": orders[i].fk_User, "status": orders_statuses[i]}
                orders_answer.append(item)
                print(orders_answer)
                print(len(orders_statuses))
            return render_template("adminorder.html", orders=orders_answer)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/personalaccount", methods=["POST", "GET"])
def personal_account():
    with Session() as session:
        blacklist = session.execute(select(BlackList.fk_User)).scalars().all()
        users = session.execute(select(Users).where(Users.id.notin_(blacklist))).scalars()
        users_json = []
        for u in users:
            item = {"id": u.id, "Phone": u.Phone, "Email": u.Email}
            users_json.append(item)
        if request.method == "POST":
            BlackList(
                fk_User=request.json["userId"]
            )
            session.add(BlackList(
                fk_User=request.json["userId"]
            ))
            session.flush()
            session.commit()
            return make_response(jsonify({"success": "true"}), 200)
    return render_template("personalaccount.html", users=users_json)


@app.route("/")
@app.route("/index")
def index():
    if 'visits' in session:
        session['visits'] = session['visits'] + 1
    else:
        session['visits'] = 1
    return render_template("index2.html", visits=session['visits'])


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user"))

    if request.method == "POST":
        phone = request.json["tel"]
        password = request.json["password"]
        with Session() as sessionn:
            blacklist = sessionn.execute(select(BlackList.fk_User)).scalars().all()
            statement = select(Users).where(
                Users.Phone == phone, Users.id.notin_(blacklist)
            )
            result = sessionn.execute(statement)
            result = result.fetchone()

            encoding_password = password.encode('utf-8')
            hashed_password = hashlib.md5(encoding_password.strip()).hexdigest()

            if result and str(hashed_password) == result[0].Password:
                print("Login Successful")
                user_login = UserLogin().create(result[0])
                login_user(user_login)
                response = make_response(jsonify({"success": "true"}), 200)
                return response
            elif not result:
                flash("Пользователь не найден", "danger")
                return make_response(jsonify({"success": "false"}), 304)
            elif str(hashed_password) != result[0].Password:
                flash("Неправильный пароль", "danger")
                return make_response(jsonify({"success": "false"}), 304)
    print(get_flashed_messages())
    return render_template("login.html")


@app.route("/order", methods=["POST", "GET"])
@login_required
def order():
    if request.method == "GET":
        with Session() as session:
            statement = select(OrderStatus.fk_Order).where(OrderStatus.fk_Status == 1)
            order_status = session.execute(statement).scalars().all()
            statement = select(Order).where(Order.fk_User == current_user.get_id(), Order.id.in_(order_status))
            order_result = session.execute(statement).fetchone()
            total_price = 0
            if order_result:
                statement = select(OrderList).where(OrderList.fk_Order == order_result[0].id).order_by(OrderList.id)
                order_list_result = session.execute(statement).scalars().all()
                dish_ids = [row.fk_Dish for row in order_list_result]

                statement = select(Dish).where(Dish.id.in_(dish_ids))
                dishes_result = session.execute(statement).scalars().all()

                order_list = [row.Amount for row in order_list_result]

                cart_items = []

                for i in range(len(dishes_result)):
                    item = {'Name': dishes_result[i].Name, 'Price': dishes_result[i].Price, "Amount": order_list[i]}
                    total_price += dishes_result[i].Price * order_list[i]
                    cart_items.append(item)
                if len(dishes_result) != 0:
                    response = make_response(jsonify(cart_items), 200)
                    response.headers['Content-Type'] = 'application/json'
                    return render_template("order.html", total_price=total_price)
                else:
                    return redirect("/basket", 200, Response=None)
        return render_template("order.html", total_price=total_price)
    if request.method == "POST":
        with Session() as session:
            statement = select(OrderStatus.fk_Order).where(OrderStatus.fk_Status == 1)
            order_status = session.execute(statement).scalars().all()
            statement = select(Order).where(Order.fk_User == current_user.get_id(), Order.id.in_(order_status))
            order_result = session.execute(statement).fetchone()

            session.execute(
                update(OrderStatus)
                .where(OrderStatus.fk_Order == order_result[0].id)
                .values(fk_Status=2)
            )

            session.execute(
                update(Order)
                .where(Order.fk_User == current_user.get_id(), Order.id.in_(order_status))
                .values(Price=str(request.json["price"])[0:-2])
            )

            order = Order(
                fk_User=current_user.get_id(),
                Price=0,
                Code=config.random_string(),
            )
            session.add(order)
            session.flush()
            session.commit()

            statement = select(Order).order_by(Order.id.desc())
            result = session.execute(statement)
            result = result.scalar()
            status = OrderStatus(
                fk_Order=result.id,
                fk_Status=1,
                Time=datetime.datetime.now().time(),
                Date=datetime.datetime.now().date(),
            )
            session.add(status)
            session.flush()
            session.commit()
            return make_response(redirect(url_for("verbron")), 200)
    return render_template("order.html")


@app.route("/indhotel", methods=["POST", "GET"])
@login_required
def ind_hotel():
    if request.method == "POST":
        print(request.json['roomName'])
        checkin_date = request.json['checkinDate']
        checkout_date = request.json['checkoutDate']
        start_date = datetime.datetime(int(checkin_date[:4]), int(checkin_date[5:7]), int(checkin_date[8:]))
        end_date = datetime.datetime(int(checkout_date[:4]), int(checkout_date[5:7]), int(checkout_date[8:]))

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        delta = end_date - start_date
        print(checkin_date, checkout_date)
        with Session() as sessionn:
            statement = select(Rooms).where(
                Rooms.Name == request.json['roomName'],
            )
            result = sessionn.execute(statement)
            result = result.fetchone()
            new_bron = Bron(
                Checkin_date=request.json['checkinDate'],
                Checkout_date=request.json['checkoutDate'],
                fk_Room=result[0].id,
                fk_User=current_user.get_id(),
                Price=delta.days * result[0].Price_Day,
                Code=config.random_string(),
            )
            sessionn.add(new_bron)
            sessionn.flush()
            sessionn.commit()
        response = make_response(redirect(url_for("verbron")))
        return response
    current_date = datetime.date.today()
    return render_template("indhotel.html", current_date=current_date)


@app.route("/hotels")
def hotels():
    return render_template("hotels.html")


@app.route("/verbron")
@login_required
def verbron():
    with Session() as sessionn:
        statement = select(Bron).where(
            Bron.fk_User == current_user.get_id(),
        )
        result = sessionn.execute(statement)
        result = result.scalars()

        code = {"code": result.all()[-1].Code}
    return render_template("verbron.html", code=code)


@app.route("/menu", methods=["POST", "GET"])
def menu():
    if request.method == "POST":
        with (Session() as session):
            statement = select(Dish).where(Dish.Name == request.json['name'])
            result = session.execute(statement)
            result = result.scalar()

            statement = select(OrderStatus.fk_Order).where(OrderStatus.fk_Status == 1)
            order_status = session.execute(statement).scalars().all()
            statement = select(Order).where(Order.fk_User == current_user.get_id(), Order.id.in_(order_status))
            result2 = session.execute(statement)
            result2 = result2.fetchone()

            statement = select(OrderList).where(OrderList.fk_Order == result2[0].id, OrderList.fk_Dish == result.id)
            result3 = session.execute(statement)
            result3 = result3.fetchone()
            if not result3:
                print("!!!!!!!!!!!!!!")
                order_list = OrderList(
                    fk_Dish=result.id,
                    Amount=1,
                    fk_Order=result2[0].id,
                )
                session.add(order_list)
            else:
                session.execute(
                    update(OrderList)
                    .where(OrderList.fk_Order == result2[0].id, OrderList.fk_Dish == result.id)
                    .values(Amount=result3[0].Amount + 1)
                )
            session.flush()
            session.commit()

    return render_template("menu.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    response = make_response(jsonify({"ok": True}), 200)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
@login_required
def user():
    if request.method == "POST":
        with Session() as session:
            session.execute(
                update(Users)
                .where(Users.id == current_user.get_id())
                .values(Name=request.json['name'], Email=request.json['email'], Surname=request.json['surname'], Phone=request.json['phone'])
            )
            session.flush()
            session.commit()
        return make_response(jsonify({"success": True}), 200)
    if request.method == "GET":
        user = current_user.get_current_user_info()
        with Session() as session:
            orders = session.execute(
                select(Order.Code, Order.Price, OrderStatus.Date, Status.Name)
                .select_from(Order).where(Order.fk_User == current_user.get_id(), Order.Price != 0)
                .join(OrderStatus, Order.id == OrderStatus.fk_Order)
                .join(Status, OrderStatus.fk_Status == Status.id)
                .where(OrderStatus.fk_Order == Order.id)
            )
            orders = orders.fetchall()
            orders_json = []
            for order in orders:
                orders_json.append({"code": order.Code, "price": order.Price, "date": order.Date, "status": order.Name})
        if user["fk_role"] == 2:
            return redirect(url_for("admin_profile"))
    return render_template("user.html", user=user, orders=orders_json)


@app.route("/basket")
@login_required
def basket():
    return render_template("basket.html")


@app.route("/shoppingcart", methods=["POST", "GET"])
@login_required
def shopping_cart_add():
    if request.method == "POST":
        with Session() as session:
            statement = select(Dish).where(Dish.Name == request.json["Name"])
            selected_dish = session.execute(statement)
            selected_dish = selected_dish.fetchone()
            print(request.json["Name"])

            statement = select(OrderStatus.fk_Order).where(OrderStatus.fk_Status == 1)
            order_status = session.execute(statement).scalars().all()
            statement = select(Order).where(Order.fk_User == current_user.get_id(), Order.id.in_(order_status))
            result2 = session.execute(statement)
            result2 = result2.fetchone()

            if request.json["delete"] == "true":
                statement = delete(OrderList).where(OrderList.fk_Dish == selected_dish[0].id, OrderList.fk_Order == result2[0].id)
                session.execute(statement)
            else:
                statement = select(OrderList).where(OrderList.fk_Dish == selected_dish[0].id, OrderList.fk_Order == result2[0].id)
                result = session.execute(statement)
                result = result.fetchone()
                session.execute(
                    update(OrderList)
                    .where(OrderList.fk_Dish == selected_dish[0].id, OrderList.fk_Order == result2[0].id)
                    .values(Amount=result[0].Amount + request.json["delta"])
                )
            session.flush()
            session.commit()

    if request.method == "GET":
        with Session() as session:
            statement = select(OrderStatus.fk_Order).where(OrderStatus.fk_Status == 1)
            order_status = session.execute(statement).scalars().all()
            statement = select(Order).where(Order.fk_User == current_user.get_id(), Order.id.in_(order_status))
            order_result = session.execute(statement).fetchone()

            if order_result:
                statement = select(OrderList).where(OrderList.fk_Order == order_result[0].id).order_by(OrderList.id)
                order_list_result = session.execute(statement).scalars().all()
                dish_ids = [row.fk_Dish for row in order_list_result]

                statement = select(Dish).where(Dish.id.in_(dish_ids))
                dishes_result = session.execute(statement).scalars().all()

                order_list = [row.Amount for row in order_list_result]

                cart_items = []

                for i in range(len(dishes_result)):
                    item = {'Name': dishes_result[i].Name, 'Price': dishes_result[i].Price, "Amount": order_list[i], "delete": "false", "Image": dishes_result[i].Image}
                    cart_items.append(item)
            print(cart_items)
        response = jsonify(cart_items)
        response.headers['Content-Type'] = 'application/json'
        return response

    return render_template("basket.html")


@app.route("/verorder", methods=["POST", "GET"])
@login_required
def veorder():
    with Session() as sessionn:
        statement = select(Order).where(
            Order.fk_User == current_user.get_id(),
        )
        result = sessionn.execute(statement)
        result = result.scalars()

        code = {"code": result.all()[-1].Code}
    return render_template("verorder.html", code=code)
