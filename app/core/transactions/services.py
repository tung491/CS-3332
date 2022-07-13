from app.core.transactions.models import (TransactionGetOnePayload, TransactionGetOneEvent, TransactionGetAllPayload,
                                          TransactionGetAllEvent, TransactionAddEvent, TransactionAddPayload,
                                          TransactionDeletePayload, TransactionDeleteEvent)
from app.core.transactions.ports.in_bound import (TransactionGetOneUseCase, TransactionGetAllUseCase,
                                                  TransactionAddUseCase, TransactionDeleteUseCase)
from app.core.transactions.ports.out_bound import TransactionDatabaseInterface


class TransactionsGetOneService(TransactionGetOneUseCase):
    def __init__(self, transaction_db_interface: TransactionDatabaseInterface):
        self.transaction_db_interface = transaction_db_interface

    def get_one(
            self,
            payload: TransactionGetOnePayload
    ) -> TransactionGetOneEvent:
        return self.transaction_db_interface.get_one_transaction(payload)


class TransactionsGetAllService(TransactionGetAllUseCase):
    def __init__(self, transaction_db_interface: TransactionDatabaseInterface):
        self.transaction_db_interface = transaction_db_interface

    def get_all(
            self,
            payload: TransactionGetAllPayload
    ) -> TransactionGetAllEvent:
        return self.transaction_db_interface.get_all_transactions(payload)


class TransactionsAddService(TransactionAddUseCase):
    def __init__(self, transaction_db_interface: TransactionDatabaseInterface):
        self.transaction_db_interface = transaction_db_interface

    def add_transaction(
            self,
            payload: TransactionAddPayload
    ) -> TransactionAddEvent:
        return self.transaction_db_interface.add_transaction(payload)


class TransactionsDeleteService(TransactionDeleteUseCase):
    def __init__(self, transaction_db_interface: TransactionDatabaseInterface):
        self.transaction_db_interface = transaction_db_interface

    def delete_transaction(
            self,
            payload: TransactionDeletePayload
    ) -> TransactionDeleteEvent:
        return self.transaction_db_interface.delete_transaction(payload)
