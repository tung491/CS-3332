import uuid
from datetime import datetime
from functools import wraps
from hashlib import sha512

import flask
import flask_login
from flask import Blueprint, render_template, flash, session, request, redirect
from flask_login import logout_user

from app.adapters.database.postgres import (PostgresCardAdapter, PostgresTransactionAdapter, PostgresSaltAdapter,
                                            PostgresUserAdapter)
from app.core.cards.models import (CardGetExtendedOnePayload, CardChangeBalancePayload, CardChangePINPayload,
                                   CardLockPayload)
from app.core.cards.services import (CardsGetExtendedOneService, CardsChangeBalanceService, CardsChangePINService,
                                     CardLockService)
from app.core.salts.models import SaltGetOnePayload
from app.core.salts.services import SaltsGetOneService
from app.core.transactions.models import TransactionAddPayload, Transaction, TransactionGetAllPayload
from app.core.transactions.services import TransactionsAddService, TransactionsGetAllService
from app.core.users.models import UserCheckSecurityAnswerPayload
from app.core.users.services import UsersCheckSecurityAnswerService

user_transactions_app = Blueprint('user_transactions_app', __name__, template_folder='templates')


@user_transactions_app.route("/")
@flask_login.login_required
def index():
    if flask_login.current_user.locked:
        return redirect("/locked")

    return render_template("user_index.html")


@user_transactions_app.route("/deposit", methods=['GET', 'POST'])
@flask_login.login_required
def deposit():
    if flask_login.current_user.locked:
        return redirect("/locked")

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
    if amount <= 0:
        flash("Invalid input! Amount must be positive", "danger")
        return render_template("user_deposit.html", balance=card.balance)
    pre_tx_balance = card.balance
    card.balance += float(amount)
    change_balance = CardsChangeBalanceService(card_adapter)
    resp = change_balance.change_balance(
            CardChangeBalancePayload(
                    number=card.number,
                    balance=card.balance
            )
    )
    transaction_adapter = PostgresTransactionAdapter()
    add_transaction = TransactionsAddService(transaction_adapter)
    add_transaction.add_transaction(
            TransactionAddPayload(
                    transaction=Transaction(
                            id=uuid.uuid4().hex,
                            user_id=card.user_id,
                            card_number=card.number,
                            debit_amount=amount,
                            credit_amount=0,
                            pre_tx_balance=pre_tx_balance,
                            post_tx_balance=card.balance,
                            message="Deposit to card",
                            timestamp=datetime.utcnow()
                    )
            )
    )

    flash("Deposit successful", "success")
    return render_template("user_deposit.html", balance=card.balance)


@user_transactions_app.route("/withdraw", methods=['GET', 'POST'])
@flask_login.login_required
def withdraw():
    if flask_login.current_user.locked:
        return redirect("/locked")

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
    if amount <= 0 or amount > card.balance:
        flash("Invalid input! Amount must be positive number and smaller than balance", "danger")
        return render_template("user_withdraw.html", balance=card.balance)
    pre_tx_balance = card.balance
    card.balance -= amount
    change_balance = CardsChangeBalanceService(card_adapter)
    resp = change_balance.change_balance(
            CardChangeBalancePayload(
                    number=card.number,
                    balance=card.balance
            )
    )
    transaction_adapter = PostgresTransactionAdapter()
    add_transaction = TransactionsAddService(transaction_adapter)
    add_transaction.add_transaction(
            TransactionAddPayload(
                    transaction=Transaction(
                            id=uuid.uuid4().hex,
                            user_id=card.user_id,
                            card_number=card.number,
                            debit_amount=0,
                            credit_amount=amount,
                            pre_tx_balance=pre_tx_balance,
                            post_tx_balance=card.balance,
                            message="Withdraw cash from card",
                            timestamp=datetime.utcnow()
                    )
            )
    )

    flash("Withdraw successful", "success")
    return render_template("user_withdraw.html", balance=card.balance)


@user_transactions_app.route("/transfer", methods=['GET', 'POST'])
@flask_login.login_required
def transfer():
    if flask_login.current_user.locked:
        return redirect("/locked")

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
    amount = flask.request.form.get("amount")
    try:
        amount = float(amount)
    except ValueError:
        flash("Invalid input! Amount must be a number", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    if amount < 0 or amount > card.balance:
        flash("Invalid input! Amount must be positive number and smaller than balance", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    if flask.request.form["debit_card_number"] == flask_login.current_user.number:
        flash("Invalid input! You can't transfer to your own card", "danger")
        return render_template("user_transfer.html", balance=card.balance)
    if isinstance(flask.request.form["debit_card_number"], int) or isinstance(
            flask.request.form["debit_card_number"], float
            ):
        flash("Invalid input! Card number must be a string", "danger")
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
    resp = change_balance_service.change_balance(
            CardChangeBalancePayload(
                    number=debit_card.number,
                    balance=debit_card.balance + amount
            )
    )
    add_transaction = TransactionsAddService(transaction_adapter)
    add_transaction.add_transaction(
            payload=TransactionAddPayload(
                    transaction=Transaction(
                            id=str(uuid.uuid4()),
                            user_id=card.user_id,
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
    payload = TransactionAddPayload(
            transaction=Transaction(
                    id=str(uuid.uuid4()),
                    card_number=debit_card.number,
                    user_id=debit_card.user_id,
                    debit_amount=amount,
                    credit_amount=0,
                    pre_tx_balance=debit_card.balance,
                    post_tx_balance=debit_card.balance + amount,
                    message=f"Receive from {card.number}",
                    timestamp=datetime.utcnow()
            )
    )
    add_transaction.add_transaction(
        payload=payload
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
    if flask_login.current_user.locked:
        return redirect("/locked")

    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetExtendedOneService(card_adapter)
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=flask_login.current_user.number
            )
    ).data
    return render_template("user_balance_enquire.html", balance=card.balance)


@user_transactions_app.route("/transactions", methods=['GET'])
@flask_login.login_required
def query_transaction():
    if flask_login.current_user.locked:
        return redirect("/locked")
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # Convert date to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    if start_date or end_date:
        if start_date and end_date:
            if start_date > end_date:
                flash("Invalid input! Start date must be before end date", "danger")
                return render_template("user_transactions.html")
        transaction_adapter = PostgresTransactionAdapter()
        transaction_get_all_service = TransactionsGetAllService(transaction_adapter)
        transactions = transaction_get_all_service.get_all(
                TransactionGetAllPayload(
                        card_number=flask_login.current_user.number, start_date=start_date, end_date=end_date
                )
        ).transactions
        return render_template(
                "user_transactions.html", transactions=transactions,
                start_date=start_date.strftime("%Y-%m-%d") if start_date else None,
                end_date=end_date.strftime("%Y-%m-%d") if end_date else None,
        )
    else:
        return render_template("user_transactions.html", transactions=[], start_date=None, end_date=None)


@user_transactions_app.route("/forgot_pin", methods=['GET', 'POST'])
def forgot_pin():
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass
        return render_template("forgot_pin.html")

    card_number = flask.request.form["forgot_card_number"]
    card_adapter = PostgresCardAdapter()
    card_get_one_service = CardsGetExtendedOneService(card_adapter)
    card = card_get_one_service.get_extended_one(
            CardGetExtendedOnePayload(
                    card_number=card_number
            )
    ).data
    if not card:
        flash("Invalid input! Card number does not exist", "danger")
        return render_template("forgot_pin.html")
    session['forgot_card_number'] = card_number
    session['forgot_user_id'] = card.user_id
    session['security_question'] = card.user.security_question
    return redirect("/check_security_question")


@user_transactions_app.route("/check_security_question", methods=['GET', 'POST'])
def check_security_question():
    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass
        return render_template("check_security_question.html", security_question=session['security_question'])
    if 'forgot_user_id' not in session:
        return redirect("/forgot_pin")
    answer = flask.request.form["answer"]
    salt_adapter = PostgresSaltAdapter()
    user_adapter = PostgresUserAdapter()
    salt_get_one_service = SaltsGetOneService(salt_adapter)
    salt_resp = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=session['forgot_user_id']
            )
    )
    salt = salt_resp.salt
    hash_security_answer = sha512(f"{answer}{salt}".encode("utf-8")).hexdigest()
    user_check_security_question_service = UsersCheckSecurityAnswerService(user_adapter)
    print(hash_security_answer)
    resp = user_check_security_question_service.check_security_answer(
            UserCheckSecurityAnswerPayload(
                    user_id=session['forgot_user_id'],
                    security_answer=hash_security_answer
            )
    )
    if not resp.match:
        flash("Invalid answer", "danger")
        session['wrong_times'] = session.get('wrong_times', 0) + 1
        if session.get('wrong_times', 0) >= 5:
            card_adapter = PostgresCardAdapter()
            card_lock_service = CardLockService(card_adapter)
            card_lock_service.lock(
                    CardLockPayload(
                            number=session['forgot_card_number']
                    )
            )
            logout_user()
            return redirect("/locked")
        return render_template("check_security_question.html", security_question=session['security_question'])
    else:
        session.pop('wrong_times', None)
        session['check_security_question'] = True
        return redirect("/reset_pin")


@user_transactions_app.route('/locked')
def locked():
    return render_template("locked.html")


@user_transactions_app.route("/reset_pin", methods=['GET', 'POST'])
def reset_pin():
    if not flask_login.current_user.is_authenticated:
        if 'forgot_card_number' not in session:
            return redirect("/forgot_pin")
        if not session.get('check_security_question'):
            return redirect("/check_security_question")
        card_number = session['forgot_card_number']
        user_id = session['forgot_user_id']
    else:
        card_number = flask_login.current_user.number
        user_id = flask_login.current_user.user_id

    if flask.request.method == "GET":
        try:
            session.pop('_flashes', None)
        except KeyError:
            pass
        return render_template("reset_pin.html")
    salt_adapter = PostgresSaltAdapter()
    card_adapter = PostgresCardAdapter()

    pin = flask.request.form["pin"]
    if not (len(pin) == 4 or len(pin) == 6):
        flask.flash("Pin must be 4 or 6 digits.", "danger")
        return render_template("reset_pin.html")
    if not all(x.isdigit() for x in pin):
        flask.flash("Pin must be digits.", "danger")
        return render_template("reset_pin.html")

    salt_get_one_service = SaltsGetOneService(salt_adapter)
    salt_resp = salt_get_one_service.get_one(
            SaltGetOnePayload(
                    user_id=user_id
            )
    )
    pin_hash = sha512(f"{pin}{salt_resp.salt}".encode("utf-8")).hexdigest()
    reset_pin_service = CardsChangePINService(card_adapter)
    reset_pin_resp = reset_pin_service.change_pin(
            CardChangePINPayload(
                    number=card_number,
                    pin_hash=pin_hash,
            )
    )
    if reset_pin_resp.success:
        session.pop('check_security_question', None)
        session.pop('forgot_card_number', None)
        session.pop('forgot_user_id', None)
        session.pop('security_question', None)
        flash("PIN changed successfully", "success")
        if flask_login.current_user.is_authenticated:
            logout_user()
        return redirect("/login")
    else:
        return render_template("reset_pin.html")
