import flask
import flask_login
from flask import Blueprint, render_template, flash

from app.adapters.database.postgres import PostgresCardAdapter
from app.core.cards.models import CardGetExtendedOnePayload, CardChangeBalancePayload
from app.core.cards.services import CardsGetExtendedOneService, CardsChangeBalanceService

user_transactions_app = Blueprint('user_transactions_app', __name__, template_folder='templates')


@user_transactions_app.route("/")
@flask_login.login_required
def index():
    return render_template("user_index.html")


@user_transactions_app.route("/deposit", methods=['GET', 'POST'])
@flask_login.login_required
def deposit():
    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetExtendedOneService(card_adapter)
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=flask_login.current_user.number
            )
    ).extended_card
    if flask.request.method == "GET":
        return render_template("user_deposit.html", balance=card.balance)
    amount = flask.request.form["amount"]
    try:
        amount = float(amount)
    except ValueError:
        flash("Invalid input! Amount must be a number", "danger")
        return render_template("user_deposit.html", balance=card.balance)
    if amount < 0:
        flash("Invalid input! Amount must be positive", "danger")
        return render_template("user_deposit.html", balance=card.balance)

    card.balance += float(amount)
    change_balance = CardsChangeBalanceService(card_adapter)
    resp = change_balance.change_balance(
        CardChangeBalancePayload(
            number=card.number,
            balance=card.balance
            )
    )
    flash("Deposit successful", "success")
    return render_template("user_deposit.html", balance=card.balance)
