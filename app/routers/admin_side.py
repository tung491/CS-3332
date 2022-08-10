import random
import string
from datetime import datetime

import flask
import flask_login
from flask import render_template, Blueprint, session, redirect

from app.adapters.database.postgres import (PostgresUserAdapter, PostgresSaltAdapter, PostgresCardAdapter,
                                            PostgresTransactionAdapter, PostgresAdminAdapter)
from app.core.admin.models import AdminGetAllPayload, AdminDeletePayload, AdminAddPayload, Admin
from app.core.admin.services import AdminsGetAllService, AdminsDeleteService, AdminsAddService
from app.core.cards.models import (Card, CardCreatePayload, CardGetAllPayload, CardGetOnePayload, CardLockPayload,
                                   CardUnlockPayload)
from app.core.cards.services import (CardsIssueService, CardsGetAllService, CardsGetOneService, CardLockService,
                                     CardsUnlockService)
from app.core.salts.models import SaltAddPayload, SaltGetOnePayload
from app.core.salts.services import SaltsAddService, SaltsGetOneService
from app.core.transactions.models import TransactionGetAllPayload
from app.core.transactions.services import TransactionsGetAllService
from app.core.users.models import UserCreatePayload, UserGetAllPayload, User, UserGetOnePayload
from app.core.users.services import UsersCreateService, UsersGetAllService, UsersGetOneService
from app.utils.encrypt import sha512_hash

admin_app = Blueprint('admin_app', __name__, template_folder='templates')


@admin_app.route('/')
@flask_login.login_required
def index():
    return render_template("admin_index.html")


@admin_app.route("/register_user", methods=["GET", "POST"])
@flask_login.login_required
def register_user():
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass

        return render_template("admin_register_user.html")
    email = flask.request.form["email"]
    name = flask.request.form["name"]
    gender = flask.request.form['gender']
    security_question = flask.request.form['security_question']
    security_answer = flask.request.form['security_answer']
    date_of_birth = flask.request.form['date_of_birth']

    if not email:
        flask.flash("Email is required.", "danger")
        return render_template("admin_register_user.html")
    if not name:
        flask.flash("Name is required.", "danger")
        return render_template("admin_register_user.html")
    if not security_question:
        flask.flash("Security question is required.", "danger")
        return render_template("admin_register_user.html")
    if not security_answer:
        flask.flash("Security answer is required.", "danger")
        return render_template("admin_register_user.html")
    if not date_of_birth:
        flask.flash("Date of birth is required.", "danger")
        return render_template("admin_register_user.html")

    user_adapter = PostgresUserAdapter()
    user_get_all_service = UsersGetAllService(user_adapter)
    all_users = user_get_all_service.get_all(UserGetAllPayload()).users
    for user in all_users:
        if user.email == email:
            flask.flash("Email already exists.", "danger")
            return render_template("admin_register_user.html")
    user_create_service = UsersCreateService(user_adapter)
    new_user = User(
            email=email,
            name=name,
            date_of_birth=date_of_birth,
            security_question=security_question,
            security_answer=security_answer,
            gender=gender
    )
    salt_adapter = PostgresSaltAdapter()
    salt_add_service = SaltsAddService(salt_adapter)
    salt_add_service.add(
            SaltAddPayload(
                    user_id=new_user.id
            )
    )
    salt_get_one_service = SaltsGetOneService(salt_adapter)
    salt_resp = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=new_user.id
            )
    )

    hash_security_answer = sha512_hash(security_answer, salt_resp.salt)
    new_user.security_answer = hash_security_answer
    user_create_service.create(
            UserCreatePayload(
                    user=new_user
            )
    )
    flask.flash("Create user successfully", "success")
    return render_template("admin_register_user.html")


@admin_app.route("/issue_card", methods=["GET", "POST"])
@flask_login.login_required
def issue_card():
    user_adapter = PostgresUserAdapter()
    user_get_all_service = UsersGetAllService(user_adapter)
    all_users = user_get_all_service.get_all(UserGetAllPayload()).users
    user_items = [(user.id, user.name) for user in all_users]
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass

        return render_template("admin_issue_card.html", user_items=user_items)

    user_id = flask.request.form["user_id"]
    if not user_id:
        flask.flash("User id is required.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    card_type = flask.request.form["card_type"]
    if not card_type:
        flask.flash("Card type is required.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    pin = flask.request.form["pin"]
    if not pin:
        flask.flash("Pin is required.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    repeat_pin = flask.request.form["repeat_pin"]
    if not repeat_pin:
        flask.flash("Repeat pin is required.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    if pin != repeat_pin:
        flask.flash("Pin and repeat pin are not match.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    if not (len(pin) == 4 or len(pin) == 6):
        flask.flash("Pin must be 4 or 6 digits.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    if not all(x.isdigit() for x in pin):
        flask.flash("Pin must be digits.", "danger")
        return render_template("admin_issue_card.html", user_items=user_items)
    salt_adapter = PostgresSaltAdapter()
    salt_get_one_service = SaltsGetOneService(salt_adapter)
    salt_resp = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=user_id
            )
    )
    # generate random 12 digit card number
    card_number = int(''.join(random.choice(string.digits) for _ in range(12)))

    pin_hash = sha512_hash(pin, salt_resp.salt)
    card = Card(
            number=card_number,
            user_id=user_id,
            type=card_type,
            pin=pin_hash,
            locked=False,
            balance=0
    )
    card_adapter = PostgresCardAdapter()
    card_create_service = CardsIssueService(card_adapter)
    card_create_service.issue(
            CardCreatePayload(card=card)
    )
    flask.flash(f"Issue card successfully. The card number is {card_number}", "success")
    return render_template("admin_issue_card.html", user_items=user_items)


@admin_app.route("/customers", methods=["GET"])
@flask_login.login_required
def list_customers():
    user_id = flask.request.args.get("user_id")
    name = flask.request.args.get("name")
    email = flask.request.args.get("email")
    gender = flask.request.args.get("gender")

    user_adapter = PostgresUserAdapter()
    user_get_all_service = UsersGetAllService(user_adapter)
    payload = UserGetAllPayload()
    if user_id:
        payload.user_id = user_id
    if name:
        payload.name = name
    if email:
        payload.email = email
    if gender:
        payload.gender = gender

    users = user_get_all_service.get_all(payload).users
    return render_template("admin_list_customers.html", users=users)


@admin_app.route("/customers/<user_id>")
@flask_login.login_required
def get_detail_customer(user_id):
    user_adapter = PostgresUserAdapter()
    user_get_one_service = UsersGetOneService(user_adapter)
    user = user_get_one_service.get_one(
            UserGetOnePayload(
                    user_id=user_id
            )
    ).user
    card_adapter = PostgresCardAdapter()
    card_get_all_service = CardsGetAllService(card_adapter)
    cards = card_get_all_service.get_all(
            CardGetAllPayload(
                    user_id=user_id
            )
    ).data
    return render_template("admin_customer_detail.html", user=user, cards=cards)


@admin_app.route("/lock_card/<card_id>", methods=["POST"])
@flask_login.login_required
def lock_card(card_id):
    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetOneService(card_adapter)
    card = card_get_one_service.get_one(
            CardGetOnePayload(
                    card_id=card_id
            )
    ).data
    if card.locked:
        flask.flash("Card is already locked.", "danger")
        return redirect(flask.request.referrer)
    card.locked = True
    card_lock_service = CardLockService(card_adapter)
    card_lock_service.lock(
            CardLockPayload(number=card.number)
    )
    flask.flash("Lock card successfully", "success")
    return redirect(flask.request.referrer)


@admin_app.route("/unlock_card/<card_id>", methods=["POST"])
@flask_login.login_required
def unlock_card(card_id):
    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetOneService(card_adapter)
    card = card_get_one_service.get_one(
            CardGetOnePayload(
                    card_id=card_id
            )
    ).data
    if not card.locked:
        flask.flash("Card is already unlocked.", "danger")
        return redirect(flask.request.referrer)
    card.locked = False
    card_unlock_service = CardsUnlockService(card_adapter)
    card_unlock_service.unlock(
            CardUnlockPayload(number=card.number)
    )
    flask.flash("Unlock card successfully", "success")
    return redirect(flask.request.referrer)


@admin_app.route("/cards", methods=["GET"])
@flask_login.login_required
def list_cards():
    card_id = flask.request.args.get("card_id", "")
    card_number = flask.request.args.get("card_number", "")
    card_type = flask.request.args.get("card_type", "")
    user_id = flask.request.args.get("user_id", "")
    locked = flask.request.args.get("locked", "")

    card_adapter = PostgresCardAdapter()
    card_get_all_service = CardsGetAllService(card_adapter)
    payload = CardGetAllPayload()
    if card_id:
        payload.card_id = card_id
    if card_number:
        payload.card_number = int(card_number)
    if card_type:
        payload.card_type = card_type
    if user_id:
        payload.user_id = user_id
    if locked:
        payload.locked = locked == "True"

    cards = card_get_all_service.get_all(payload).data
    return render_template("admin_list_cards.html", cards=cards)


@admin_app.route("/transactions", methods=['GET'])
@flask_login.login_required
def query_transaction():
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass

    start_date = flask.request.args.get('start_date')
    end_date = flask.request.args.get('end_date')
    user_id = flask.request.args.get('user_id', "")
    card_number = flask.request.args.get('card_number', None)
    # Convert date to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    transaction_adapter = PostgresTransactionAdapter()
    transaction_get_all_service = TransactionsGetAllService(transaction_adapter)
    payload = TransactionGetAllPayload()
    if start_date and end_date:
        if start_date > end_date:
            flask.flash("Start date must be earlier than end date", "danger")
            return redirect(flask.request.referrer)
    if start_date:
        payload.start_date = start_date
    if end_date:
        payload.end_date = end_date
    if user_id:
        payload.user_id = user_id
    if card_number:
        payload.card_number = int(card_number)
    transactions = transaction_get_all_service.get_all(payload).transactions
    return render_template(
            "admin_transactions.html", transactions=transactions,
            start_date=start_date.strftime("%Y-%m-%d") if start_date else "",
            end_date=end_date.strftime("%Y-%m-%d") if end_date else "",
            user_id=user_id, card_number=card_number or ""
    )


@admin_app.route("/admins")
@flask_login.login_required
def list_admins():
    admin_id = flask.request.args.get("id", "")
    name = flask.request.args.get("name", "")
    email = flask.request.args.get("email", "")

    admin_adapter = PostgresAdminAdapter()
    admin_get_all_service = AdminsGetAllService(admin_adapter)
    payload = AdminGetAllPayload()
    if admin_id:
        payload.admin_id = admin_id
    if name:
        payload.name = name
    if email:
        payload.email = email
    admins = admin_get_all_service.get_all(payload).admins

    return render_template("admin_list_admin.html", admins=admins)


@admin_app.route("/delete_admin/<admin_id>", methods=["DELETE", "POST"])
@flask_login.login_required
def delete_admin(admin_id):
    admin_adapter = PostgresAdminAdapter()
    admin_delete_service = AdminsDeleteService(admin_adapter)
    admin_delete_service.delete_admin(
            AdminDeletePayload(admin_id=admin_id)
    )
    flask.flash("Delete admin successfully", "success")
    return redirect(flask.request.referrer)


@admin_app.route("/add_admin", methods=["GET", "POST"])
@flask_login.login_required
def add_admin():
    if flask.request.method == "GET":
        return render_template("admin_add_admin.html")
    name = flask.request.form.get("name")
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    repeat_password = flask.request.form.get("repeat_password")
    if not name:
        flask.flash("Name is required", "danger")
        return render_template("admin_add_admin.html")
    if not email:
        flask.flash("Email is required", "danger")
        return render_template("admin_add_admin.html")

    if not password:
        flask.flash("Password is required", "danger")
        return render_template("admin_add_admin.html")
    if password != repeat_password:
        flask.flash("Password does not match", "danger")
        return render_template("admin_add_admin.html")
    admin_adapter = PostgresAdminAdapter()
    admin_get_all_service = AdminsGetAllService(admin_adapter)
    admins = admin_get_all_service.get_all(
            AdminGetAllPayload()
    ).admins
    for admin in admins:
        if admin.email == email:
            flask.flash("Email already exists", "danger")
            return render_template("admin_add_admin.html")

    new_admin = Admin(
            name=name,
            email=email,
            password_hash=password
    )
    salt_adapter = PostgresSaltAdapter()
    salt_add_service = SaltsAddService(salt_adapter)
    salt_add_service.add(
            SaltAddPayload(
                    user_id=new_admin.id,
            )
        )
    salt_get_one_service = SaltsGetOneService(salt_adapter)
    salt = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=new_admin.id,
            )
    ).salt

    new_admin.password_hash = sha512_hash(password, salt)

    admin_adapter = PostgresAdminAdapter()
    admin_add_service = AdminsAddService(admin_adapter)
    admin_add_service.add_admin(
            AdminAddPayload(
                    admin=new_admin,
            )
    )
    flask.flash("Add admin successfully", "success")
    return render_template("admin_add_admin.html")


