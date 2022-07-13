from app.adapters.database.postgres import PostgresTransactionAdapter
from app.core.transactions.services import (TransactionsGetOneService, TransactionsGetAllService,
                                            TransactionsAddService,
                                            TransactionsDeleteService)


def transaction_interface() -> PostgresTransactionAdapter:
    return PostgresTransactionAdapter()


def transaction_get_one_service(
        transaction_db_interface: PostgresTransactionAdapter,
) -> TransactionsGetOneService:
    return TransactionsGetOneService(transaction_db_interface)


def transaction_get_all_service(
        transaction_db_interface: PostgresTransactionAdapter,
) -> TransactionsGetAllService:
    return TransactionsGetAllService(transaction_db_interface)


def transaction_add_service(
        transaction_db_interface: PostgresTransactionAdapter,
) -> TransactionsAddService:
    return TransactionsAddService(transaction_db_interface)


def transaction_delete_service(
        transaction_db_interface: PostgresTransactionAdapter,
) -> TransactionsDeleteService:
    return TransactionsDeleteService(transaction_db_interface)
