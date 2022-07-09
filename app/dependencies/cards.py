from app.adapters.database.postgres import PostgresCardAdapter
from app.core.cards.ports.out_bound import CardDatabaseInterface
from app.core.cards.services import (CardsGetOneService, CardsGetAllService, CardsIssueService, CardLockService,
                                     CardsUnlockService, CardsChangeBalanceService, CardsCheckPINService,
                                     CardsChangePINService)


def card_interface() -> PostgresCardAdapter:
    return PostgresCardAdapter()


def card_get_one_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsGetOneService:
    return CardsGetOneService(card_db_interface)


def card_get_all_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsGetAllService:
    return CardsGetAllService(card_db_interface)


def card_issue_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsGetOneService:
    return CardsIssueService(card_db_interface)


def card_lock_service(
        card_db_interface: CardDatabaseInterface,
) -> CardLockService:
    return CardLockService(card_db_interface)


def card_unlock_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsUnlockService:
    return CardsUnlockService(card_db_interface)


def card_change_balance_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsChangeBalanceService:
    return CardsChangeBalanceService(card_db_interface)


def card_check_pin_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsCheckPINService:
    return CardsCheckPINService(card_db_interface)


def card_change_pin_service(
        card_db_interface: CardDatabaseInterface,
) -> CardsChangePINService:
    return CardsChangePINService(card_db_interface)
