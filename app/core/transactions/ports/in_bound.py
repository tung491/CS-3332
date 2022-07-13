from typing import Protocol

from app.core.transactions.models import (TransactionGetOnePayload, TransactionGetOneEvent, TransactionGetAllPayload,
                                          TransactionGetAllEvent, TransactionAddPayload, TransactionAddEvent,
                                          TransactionDeletePayload, TransactionDeleteEvent)


class TransactionGetOneUseCase(Protocol):
    def get_one(
            self,
            payload: TransactionGetOnePayload
    ) -> TransactionGetOneEvent:
        ...


class TransactionGetAllUseCase(Protocol):
    def get_all(
            self,
            payload: TransactionGetAllPayload
    ) -> TransactionGetAllEvent:
        ...


class TransactionAddUseCase(Protocol):
    def add_transaction(
            self,
            payload: TransactionAddPayload
    ) -> TransactionAddEvent:
        ...


class TransactionDeleteUseCase(Protocol):
    def delete_transaction(
            self,
            payload: TransactionDeletePayload
    ) -> TransactionDeleteEvent:
        ...
