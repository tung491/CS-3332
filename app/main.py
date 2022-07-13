from hashlib import sha512

import flask
import flask_login
from flask import Flask, flash, redirect, session
from flask_login import LoginManager, login_required, logout_user

from app.adapters.database.postgres import PostgresUserAdapter, PostgresCardAdapter, PostgresSaltAdapter
from app.core.cards.models import CardGetOnePayload, CardCheckPINPayload, ExtendedCard, CardGetExtendedOnePayload
from app.core.cards.services import CardsGetOneService, CardsGetExtendedOneService
from app.core.salts.models import SaltGetOnePayload
from app.core.salts.services import SaltsGetOneService
from app.core.users.models import UserGetOnePayload
from app.dependencies.cards import card_check_pin_service
from app.routers.user_side import user_transactions_app
from app.settings import Settings


def init_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Settings().dict())
    return app


login_manager = LoginManager()
app = init_app()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager.init_app(app)


app.register_blueprint(user_transactions_app)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return flask.render_template("login_form.html")
    card_number = flask.request.form["card_number"]
    pin = flask.request.form["pin"]
    salt_adapter = PostgresSaltAdapter()
    card_adapter = PostgresCardAdapter()
    salt_get_one_service = SaltsGetOneService(salt_adapter)
    card_get_one_service = CardsGetExtendedOneService(card_adapter)

    card_resp = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=card_number,
            )
    )
    salt_resp = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=card_resp.data.user_id,
            )
    )
    pin_hash = sha512(f"{pin}{salt_resp.salt}".encode("utf-8")).hexdigest()
    check_pin_service = card_check_pin_service(card_adapter)
    check_pin_resp = check_pin_service.check_pin(
            CardCheckPINPayload(
                    number=card_number,
                    pin_hash=pin_hash,
            )
    )
    if check_pin_resp.match:
        flask_login.login_user(card_resp.data)
        flask.flash('Logged in successfully.')
        return flask.redirect("/")
    else:
        print("no match")
        flask.flash('Incorrect card number or PIN.')
        return "Invalid card number or PIN"


@app.route("/logout")
@flask_login.login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_card(id):
    if id is None:
        redirect('/login')
    try:
        card_adapter = PostgresCardAdapter()
        card_get_one_service = CardsGetExtendedOneService(card_adapter)
        card = card_get_one_service.get_extended_one(
                CardGetExtendedOnePayload(
                        card_number=int(id),
                )).data
    except Exception:
        return None
    if card.is_active:
        return card
    else:
        return None
