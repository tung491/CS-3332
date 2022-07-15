import uuid
from datetime import datetime

import flask
import flask_login
from flask import Blueprint, render_template, flash, session

from app.adapters.database.postgres import PostgresCardAdapter, PostgresTransactionAdapter
from app.core.cards.models import CardGetExtendedOnePayload, CardChangeBalancePayload
from app.core.cards.services import CardsGetExtendedOneService, CardsChangeBalanceService
from app.core.transactions.models import TransactionAddPayload, Transaction
from app.core.transactions.services import TransactionsAddService

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
    ).data
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass
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


@user_transactions_app.route("/withdraw", methods=['GET', 'POST'])
@flask_login.login_required
def withdraw():
    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetExtendedOneService(card_adapter)
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=flask_login.current_user.number
            )
    ).data
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass
        return render_template("user_withdraw.html", balance=card.balance)
    amount = flask.request.form["amount"]
    try:
        amount = float(amount)
    except ValueError:
        flash("Invalid input! Amount must be a number", "danger")
        return render_template("user_withdraw.html", balance=card.balance)
    if amount < 0 or amount > card.balance:
        flash("Invalid input! Amount must be positive number and smaller than balance", "danger")
        return render_template("user_withdraw.html", balance=card.balance)

    card.balance -= amount
    change_balance = CardsChangeBalanceService(card_adapter)
    resp = change_balance.change_balance(
            CardChangeBalancePayload(
                    number=card.number,
                    balance=card.balance
            )
    )
    flash("Withdraw successful", "success")
    return render_template("user_withdraw.html", balance=card.balance)


@user_transactions_app.route("/transfer", methods=['GET', 'POST'])
@flask_login.login_required
def transfer():
    card_adapter = PostgresCardAdapter()
    transaction_adapter = PostgresTransactionAdapter()
    card_get_one_service = CardsGetExtendedOneService(card_adapter)
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=flask_login.current_user.number
            )
    ).data
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass
        return render_template("user_transfer.html", balance=card.balance)
    amount = flask.request.form["amount"]
    try:
        amount = float(amount)
    except ValueError:
        flash("Invalid input! Amount must be a number", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    if amount < 0 or amount > card.balance:
        flash("Invalid input! Amount must be positive number and smaller than balance", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    debit_card_resp = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=flask.request.form["debit_card_number"]
            )
    )
    if not debit_card_resp.success:
        flash("Invalid input! Target card number does not exist", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    debit_card = debit_card_resp.data
    change_balance_service = CardsChangeBalanceService(card_adapter)
    resp = change_balance_service.change_balance(
            CardChangeBalancePayload(
                    number=card.number,
                    balance=card.balance - amount
            )
    )
    if not resp.success:
        flash("Transfer failed", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    print(debit_card)
    resp = change_balance_service.change_balance(
            CardChangeBalancePayload(
                    number=debit_card.number,
                    balance=debit_card.balance + amount
            )
    )
    add_transaction = TransactionsAddService(transaction_adapter)
    add_transaction.add_transaction(
            TransactionAddPayload(
                    transaction=Transaction(
                            id = uuid.uuid4().hex,
                            card_number=card.number,
                            debit_amount=0,
                            credit_amount=amount,
                            pre_tx_balance=card.balance,
                            post_tx_balance=card.balance - amount,
                            message=f"Transfer to {debit_card.number}",
                            timestamp=datetime.utcnow()
                    )
            )
    )
    add_transaction.add_transaction(
            TransactionAddPayload(
                    transaction=Transaction(
                            id=uuid.uuid4().hex,
                            card_number=debit_card.number,
                            debit_amount=amount,
                            credit_amount=0,
                            pre_tx_balance=debit_card.balance,
                            post_tx_balance=debit_card.balance + amount,
                            message=f"Receive from {card.number}",
                            timestamp=datetime.utcnow()
                    )
            )
    )
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=card.number
            )
    ).data
    flash("Transfer successful", "success")
    return render_template("user_transfer.html", balance=card.balance)


@user_transactions_app.route("/balance-enquiry", methods=['GET'])
@flask_login.login_required
def balance():
    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetExtendedOneService(card_adapter)
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=flask_login.current_user.number
            )
    ).data
    return render_template("user_balance_enquire.html", balance=card.balance)