from abc import abstractmethod, ABC

from app.core.cards.models import (CardGetOnePayload, CardGetOneEvent, CardGetAllPayload,
                                   CardGetAllEvent, CardLockPayload, CardLockEvent, CardCreateEvent, CardCreatePayload,
                                   CardUnlockPayload, CardUnlockEvent, CardChangeBalancePayload, CardChangeBalanceEvent,
                                   CardCheckPINPayload, CardCheckPINEvent, CardChangePINPayload, CardChangePINEvent,
                                   CardGetExtendedOnePayload, CardGetExtendedOneEvent)


class CardDatabaseInterface(ABC):
    @abstractmethod
    def get_one(
            self,
            payload: CardGetOnePayload
    ) -> CardGetOneEvent:
        ...

    @abstractmethod
    def get_all(
            self,
            payload: CardGetAllPayload
    ) -> CardGetAllEvent:
        ...

    @abstractmethod
    def issues_card(
            self,
            payload: CardCreatePayload
    ) -> CardCreateEvent:
        ...

    @abstractmethod
    def lock_card(
            self,
            payload: CardLockPayload
    ) -> CardLockEvent:
        ...

    @abstractmethod
    def unlock_card(
            self,
            payload: CardUnlockPayload
    ) -> CardUnlockEvent:
        ...

    @abstractmethod
    def change_balance(
            self,
            payload: CardChangeBalancePayload
    ) -> CardChangeBalanceEvent:
        ...

    @abstractmethod
    def check_pin(
            self,
            payload: CardCheckPINPayload
    ) -> CardCheckPINEvent:
        ...

    @abstractmethod
    def change_pin(
            self,
            payload: CardChangePINPayload
    ) -> CardChangePINEvent:
        ...

    @abstractmethod
    def get_extended_one(
            self,
            payload: CardGetExtendedOnePayload
    ) -> CardGetExtendedOneEvent:
        ...
