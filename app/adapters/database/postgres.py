from datetime import datetime
from datetime import datetime
from typing import Optional, List

from flask import current_app
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, Text, DateTime, select, Boolean, Float
)

from app.core.cards.models import (CardChangePINPayload, CardChangePINEvent, CardCheckPINPayload, CardCheckPINEvent,
                                   CardChangeBalancePayload, CardChangeBalanceEvent, CardUnlockPayload, CardUnlockEvent,
                                   CardLockPayload, CardLockEvent, CardCreatePayload, CardCreateEvent,
                                   CardGetAllPayload, CardGetAllEvent, CardGetOnePayload, CardGetOneEvent, Card,
                                   CardGetExtendedOnePayload, CardGetExtendedOneEvent, ExtendedCard)
from app.core.cards.ports.out_bound import CardDatabaseInterface
from app.core.salts.models import SaltGetOnePayload, SaltGetOneEvent, SaltAddPayload, SaltAddEvent
from app.core.salts.ports.out_bound import SaltDatabaseInterface
from app.core.transactions.models import (TransactionDeletePayload, TransactionDeleteEvent, TransactionAddPayload,
                                          TransactionAddEvent, TransactionGetAllPayload, TransactionGetAllEvent,
                                          TransactionGetOnePayload, TransactionGetOneEvent, Transaction)
from app.core.transactions.ports.out_bound import TransactionDatabaseInterface
from app.core.users.models import (User, UserGetOnePayload, UserGetOneEvent, UserCreatePayload, UserCreateEvent,
                                   UserGetAllPayload, UserGetAllEvent, UserDeletePayload, UserDeleteEvent,
                                   UserCheckSecurityAnswerPayload, UserCheckSecurityAnswerEvent)
from app.core.users.ports.out_bound import UserDatabaseInterface
from app.settings import get_app_settings

settings = get_app_settings()
engine = create_engine(settings.POSTGRES_DATABASE_URL)
metadata = MetaData()

users_table = Table(
        'users', metadata,
        Column('id', Text, primary_key=True),
        Column('name', Text),
        Column('date_of_birth', DateTime),
        Column('email', Text),
        Column('gender', Text),
        Column('security_question', Text),
        Column('security_answer', Text)
)

salts_table = Table(
        'salts', metadata,
        Column('user_id', Text, primary_key=True),
        Column('salt', Text)
)

cards_table = Table(
        'cards', metadata,
        Column('number', Integer, primary_key=True),
        Column('user_id', Text),
        Column('pin', Text),
        Column('type', Text),
        Column('locked', Boolean),
        Column('balance', Float)
)

transactions_table = Table(
        'transactions', metadata,
        Column('id', Text, primary_key=True),
        Column('debit_account_id', Text),
        Column('credit_account_id', Text),
        Column('withdrawal_amount', Float),
        Column('deposit_amount', Float),
        Column('pre_tx_balance', Float),
        Column('post_tx_balance', Float),
        Column('message', Text),
        Column('date', DateTime)
)


class PostgresInterface:
    def __init__(self):
        self.connection = engine.connect()


class PostgresUserAdapter(UserDatabaseInterface, PostgresInterface):
    def get_one(self, payload: UserGetOnePayload) -> UserGetOneEvent:
        with self.connection.begin():
            user = self.connection.execute(
                    select(
                            [users_table.c.id, users_table.c.name, users_table.c.date_of_birth, users_table.c.email,
                             users_table.c.security_question, users_table.c.security_answer, users_table.c.gender]
                    )
                    .where(users_table.c.id == payload.user_id)
            ).fetchone()
            if user is None:
                raise Exception('User not found')
            print(user.date_of_birth, user.gender)
            return UserGetOneEvent(
                    user=User(
                            name=user.name,
                            id=user.id,
                            date_of_birth=user.date_of_birth,
                            email=user.email,
                            security_question=user.security_question,
                            security_answer=user.security_answer,
                            gender=user.gender
                    ),
            )

    def get_all(self, payload: UserGetAllPayload) -> UserGetAllEvent:
        with self.connection.begin():
            query = users_table.select()

            if payload.name:
                query = query.where(users_table.c.name == payload.name)
            if payload.email:
                query = query.where(users_table.c.email == payload.email)
            if payload.gender:
                query = query.where(users_table.c.gender == payload.gender)
            if payload.date_of_birth:
                query = query.where(users_table.c.date_of_birth == payload.date_of_birth)
            users = query.fetchall()
            users = [
                User(
                        name=user.name,
                        id=user.id,
                        date_of_birth=user.date_of_birth,
                        email=user.email,
                        security_question=user.security_question,
                        security_answer=user.security_answer,
                )
                for user in users
            ]
            return UserGetAllEvent(
                    users=users,
            )

    def add_user(self, payload: UserCreatePayload) -> UserCreateEvent:
        with self.connection.begin():
            self.connection.execute(
                    users_table.insert().values(
                            name=payload.user.name,
                            date_of_birth=payload.user.date_of_birth,
                            email=payload.user.email,
                            security_question=payload.user.security_question,
                            security_answer=payload.user.security_answer,
                    )
            )
            user = self.get_all(UserGetAllPayload(name=payload.user.name)).users[0]
            return UserCreateEvent(
                    user=user,
            )

    def delete_user(self, payload: UserDeletePayload) -> UserDeleteEvent:
        with self.connection.begin():
            self.connection.execute(
                    users_table.delete().where(users_table.c.id == payload.user_id)
            )
        return UserDeleteEvent()

    def check_security_answer(self, payload: UserCheckSecurityAnswerPayload) -> UserCheckSecurityAnswerEvent:
        with self.connection.begin():
            user = self.connection.execute(
                    select(
                            [users_table.c.id, users_table.c.name, users_table.c.date_of_birth, users_table.c.email,
                             users_table.c.security_question, users_table.c.security_answer]
                    )
                    .where(users_table.c.id == payload.user_id)
            ).fetchone()
            if user is None:
                raise Exception('User not found')
            return UserCheckSecurityAnswerEvent(
                    match=user.security_answer == payload.security_answer
            )


class PostgresSaltAdapter(SaltDatabaseInterface, PostgresInterface):
    def get_salt(self, payload: SaltGetOnePayload) -> SaltGetOneEvent:
        with self.connection.begin():
            salt = self.connection.execute(
                    select(
                            [salts_table.c.user_id, salts_table.c.salt]
                    )
                    .where(salts_table.c.user_id == payload.user_id)
            ).fetchone()
            if salt is None:
                raise Exception('Salt not found')
            return SaltGetOneEvent(
                    user_id=salt.user_id,
                    salt=salt.salt
            )

    def add_salt(self, payload: SaltAddPayload) -> SaltAddEvent:
        with self.connection.begin():
            self.connection.execute(
                    salts_table.insert().values(
                            user_id=payload.user_id,
                            salt=payload.salt,
                    )
            )
        return SaltAddEvent(
                data=payload.salt
        )

    def delete_salt(self, payload: SaltGetOnePayload) -> SaltGetOneEvent:
        with self.connection.begin():
            self.connection.execute(
                    salts_table.delete().where(salts_table.c.user_id == payload.user_id)
            )
        return SaltGetOneEvent(
                salt=None
        )


class PostgresTransactionAdapter(TransactionDatabaseInterface, PostgresInterface):
    def get_one_transaction(self, payload: TransactionGetOnePayload) -> TransactionGetOneEvent:
        with self.connection.begin():
            transaction = self.connection.execute(
                    select(
                            [transactions_table.c.id, transactions_table.c.debit_account_id,
                             transactions_table.c.credit_account_id,
                             transactions_table.c.withdrawal_amount, transactions_table.c.deposit_amount,
                             transactions_table.c.pre_tx_balance,
                             transactions_table.c.post_tx_balance, transactions_table.c.message,
                             transactions_table.c.date]
                    )
                    .where(transactions_table.c.id == payload.trx_id)
            ).fetchone()
            if transaction is None:
                raise Exception('Transaction not found')
            return TransactionGetOneEvent(
                    transaction=Transaction(
                            id=transaction.id,
                            debit_account_id=transaction.debit_account_id,
                            credit_account_id=transaction.credit_account_id,
                            withdrawal_amount=transaction.withdrawal_amount,
                            deposit_amount=transaction.deposit_amount,
                            pre_tx_balance=transaction.pre_tx_balance,
                            post_tx_balance=transaction.post_tx_balance,
                            message=transaction.message,
                            date=transaction.date
                    )
            )

    def get_all_transactions(self, payload: TransactionGetAllPayload) -> TransactionGetAllEvent:
        with self.connection.begin():
            query = transactions_table.select()
            if payload.debit_account_id:
                query = query.where(transactions_table.c.debit_account_id == payload.debit_account_id)
            if payload.credit_account_id:
                query = query.where(transactions_table.c.credit_account_id == payload.credit_account_id)
            if payload.start_date:
                query = query.where(transactions_table.c.date >= payload.start_date)
            if payload.end_date:
                query = query.where(transactions_table.c.date <= payload.end_date)
            transactions = query.fetchall()
            transactions = [
                Transaction(
                        id=transaction.id,
                        debit_account_id=transaction.debit_account_id,
                        credit_account_id=transaction.credit_account_id,
                        withdrawal_amount=transaction.withdrawal_amount,
                        deposit_amount=transaction.deposit_amount,
                        pre_tx_balance=transaction.pre_tx_balance,
                        post_tx_balance=transaction.post_tx_balance,
                        message=transaction.message,
                        date=transaction.date
                )
                for transaction in transactions
            ]
            return TransactionGetAllEvent(
                    transactions=transactions
            )

    def add_transaction(self, payload: TransactionAddPayload) -> TransactionAddEvent:
        with self.connection.begin():
            self.connection.execute(
                    transactions_table.insert().values(
                            debit_account_id=payload.transaction.debit_account_id,
                            credit_account_id=payload.transaction.credit_account_id,
                            withdrawal_amount=payload.transaction.withdrawal_amount,
                            deposit_amount=payload.transaction.deposit_amount,
                            pre_tx_balance=payload.transaction.pre_tx_balance,
                            post_tx_balance=payload.transaction.post_tx_balance,
                            message=payload.transaction.message,
                            date=payload.transaction.date,
                    )
            )
        return TransactionAddEvent(
                transaction=payload.transaction
        )

    def delete_transaction(self, payload: TransactionDeletePayload) -> TransactionDeleteEvent:
        with self.connection.begin():
            self.connection.execute(
                    transactions_table.delete().where(transactions_table.c.id == payload.trx_id)
            )
        return TransactionDeleteEvent(
                data={}
        )


class PostgresCardAdapter(CardDatabaseInterface, PostgresInterface):

    def get_extended_one(self, payload: CardGetExtendedOnePayload) -> CardGetExtendedOneEvent:
        with self.connection.begin():
            card = self.connection.execute(
                    select(
                            [
                                cards_table.c.user_id,
                                cards_table.c.number,
                                cards_table.c.type,
                                cards_table.c.locked,
                                cards_table.c.balance,
                                cards_table.c.pin,
                                users_table.c.id, users_table.c.name, users_table.c.date_of_birth, users_table.c.email,
                                users_table.c.security_question, users_table.c.security_answer, users_table.c.gender
                            ]
                    )
                    .where(cards_table.c.number == payload.card_number)
            ).fetchone()
        print(card)
        extended_card = ExtendedCard(
                number=card.number,
                user_id=card.user_id,
                pin=card.pin,
                type=card.type,
                locked=card.locked,
                balance=card.balance,
                id=card.number,
                user=User(
                        name=card.name,
                        id=card.id,
                        date_of_birth=card.date_of_birth,
                        email=card.email,
                        security_question=card.security_question,
                        security_answer=card.security_answer,
                        gender=card.gender
                )
        )

        return CardGetExtendedOneEvent(
                extended_card=extended_card
        )

    def get_one(self, payload: CardGetOnePayload) -> CardGetOneEvent:
        with self.connection.begin():
            card = self.connection.execute(
                    select(
                            [
                                cards_table.c.user_id,
                                cards_table.c.number,
                                cards_table.c.type,
                                cards_table.c.locked,
                                cards_table.c.balance,
                                cards_table.c.pin
                            ]
                    )
                    .where(cards_table.c.number == payload.card_number)
            ).fetchone()
            if card is None:
                raise Exception('Card not found')
            return CardGetOneEvent(
                    data=Card(
                            number=card.number,
                            user_id=card.user_id,
                            pin=card.pin,
                            type=card.type,
                            locked=card.locked,
                            balance=card.balance,
                    )
            )

    def get_all(self, payload: CardGetAllPayload) -> CardGetAllEvent:
        with self.connection.begin():
            query = cards_table.select()
            if payload.user_id:
                query = query.where(cards_table.c.user_id == payload.user_id)
            if payload.card_type:
                query = query.where(cards_table.c.card_type == payload.card_type)
            cards = query.fetchall()
            cards = [
                Card(
                        number=card.number,
                        user_id=card.user_id,
                        pin=card.pin,
                        type=card.card_type,
                        locked=card.locked,
                        balance=card.balance,
                )
                for card in cards
            ]
            return CardGetAllEvent(
                    cards=cards
            )

    def issues_card(self, payload: CardCreatePayload) -> CardCreateEvent:
        with self.connection.begin():
            self.connection.execute(
                    cards_table.insert().values(
                            user_id=payload.card.user_id,
                            number=payload.card.number,
                            pin=payload.card.pin,
                            type=payload.card.type,
                            locked=payload.card.locked,
                            balance=payload.card.balance,
                    )
            )
        return CardCreateEvent(
                card=payload.card
        )

    def lock_card(self, payload: CardLockPayload) -> CardLockEvent:
        with self.connection.begin():
            self.connection.execute(
                    cards_table.update().where(cards_table.c.number == payload.number).values(
                            locked=True
                    )
            )
        return CardLockEvent(
                data={'locked': True}
        )

    def unlock_card(self, payload: CardUnlockPayload) -> CardUnlockEvent:
        with self.connection.begin():
            self.connection.execute(
                    cards_table.update().where(cards_table.c.number == payload.number).values(
                            locked=False
                    )
            )
        return CardUnlockEvent(
                data={'locked': False}
        )

    def change_balance(self, payload: CardChangeBalancePayload) -> CardChangeBalanceEvent:
        with self.connection.begin():
            self.connection.execute(
                    cards_table.update().where(cards_table.c.number == payload.number).values(
                            balance=payload.balance
                    )
            )
        return CardChangeBalanceEvent(
                data={'balance': payload.balance}
        )

    def check_pin(self, payload: CardCheckPINPayload) -> CardCheckPINEvent:
        with self.connection.begin():
            card = self.connection.execute(
                    select(
                            [cards_table.c.pin]
                    )
                    .where(cards_table.c.number == payload.number)
            ).fetchone()
            if card is None:
                raise Exception('Card not found')
            pin_match = card.pin == payload.pin_hash
            return CardCheckPINEvent(
                    match=pin_match
            )

    def change_pin(self, payload: CardChangePINPayload) -> CardChangePINEvent:
        with self.connection.begin():
            self.connection.execute(
                    cards_table.update().where(cards_table.c.number == payload.number).values(
                            pin=payload.pin_hash
                    )
            )
        return CardChangePINEvent(
                data={'pin': payload.pin_hash}
        )
