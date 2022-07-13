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

    def get_all(
            self,
            payload: TransactionGetAllPayload
    ) -> TransactionGetAllEvent:
        ...

    def add_transaction(
            self,
            payload: TransactionAddPayload
    ) -> TransactionAddEvent:
        ...

    def delete_transaction(
            self,
            payload: TransactionDeletePayload
    ) -> TransactionDeleteEvent:
        ...
