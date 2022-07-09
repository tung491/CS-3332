from app.core.cards.models import (CardGetOnePayload, CardGetOneEvent, CardGetAllEvent, CardGetAllPayload,
                                   CardCreatePayload, CardCreateEvent, CardLockEvent, CardLockPayload, CardUnlockEvent,
                                   CardUnlockPayload, CardChangeBalancePayload, CardChangeBalanceEvent,
                                   CardCheckPINPayload, CardCheckPINEvent, CardChangePINPayload, CardChangePINEvent,
                                   CardGetExtendedOnePayload, CardGetExtendedOneEvent)
from app.core.cards.ports.in_bound import (CardsGetOneUseCase, CardsGetAllUseCase, CardsIssueUseCase, CardsLockUseCase,
                                           CardsUnlockUseCase, CardsChangeBalanceUseCase, CardsCheckPINUseCase,
                                           CardsChangePINUseCase, CardsGetExtendedOneUseCase)
from app.core.cards.ports.out_bound import CardDatabaseInterface


class CardsGetOneService(CardsGetOneUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def get_one(
            self
            , payload: CardGetOnePayload
            ) -> CardGetOneEvent:
        return self.card_db_interface.get_one(payload)


class CardsGetAllService(CardsGetAllUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def get_all(
            self,
            payload: CardGetAllPayload
            ) -> CardGetAllEvent:
        return self.card_db_interface.get_all(payload)


class CardsIssueService(CardsIssueUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def issue(
            self,
            payload: CardCreatePayload
            ) -> CardCreateEvent:
        return self.card_db_interface.issues_card(payload)


class CardLockService(CardsLockUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def lock(
            self,
            query: CardLockPayload
            ) -> CardLockEvent:
        return self.card_db_interface.lock_card(query)


class CardsUnlockService(CardsUnlockUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def unlock(
            self,
            payload: CardUnlockPayload
            ) -> CardUnlockEvent:
        return self.card_db_interface.unlock_card(payload)


class CardsChangeBalanceService(CardsChangeBalanceUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def change_balance(
            self,
            payload: CardChangeBalancePayload
            ) -> CardChangeBalanceEvent:
        return self.card_db_interface.change_balance(payload)


class CardsCheckPINService(CardsCheckPINUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def check_pin(
            self,
            payload: CardCheckPINPayload
            ) -> CardCheckPINEvent:
        return self.card_db_interface.check_pin(payload)


class CardsChangePINService(CardsChangePINUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def change_pin(
            self,
            payload: CardChangePINPayload
            ) -> CardChangePINEvent:
        return self.card_db_interface.change_pin(payload)


class CardsGetExtendedOneService(CardsGetExtendedOneUseCase):
    def __init__(self, card_db_interface: CardDatabaseInterface):
        self.card_db_interface = card_db_interface

    def get_extended_one(
            self,
            payload: CardGetExtendedOnePayload
            ) -> CardGetExtendedOneEvent:
        return self.card_db_interface.get_extended_one(payload)
