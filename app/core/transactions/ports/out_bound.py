from abc import ABC, abstractmethod

from app.core.transactions.models import (TransactionGetOnePayload, TransactionGetOneEvent, TransactionGetAllPayload,
                                          TransactionGetAllEvent, TransactionAddPayload, TransactionAddEvent,
                                          TransactionDeletePayload, TransactionDeleteEvent)


class TransactionDatabaseInterface(ABC):
    @abstractmethod
    def get_one_transaction(
            self,
            payload: TransactionGetOnePayload
    ) -> TransactionGetOneEvent:
        ...

    @abstractmethod
    def get_all_transactions(
            self,
            payload: TransactionGetAllPayload
    ) -> TransactionGetAllEvent:
        ...

    @abstractmethod
    def add_transaction(
            self,
            payload: TransactionAddPayload
    ) -> TransactionAddEvent:
        ...

    @abstractmethod
    def delete_transaction(
            self,
            payload: TransactionDeletePayload
    ) -> TransactionDeleteEvent:
        ...
