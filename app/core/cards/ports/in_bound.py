from typing import Protocol

from app.core.cards.models import (CardGetOneEvent, CardGetOnePayload, CardGetAllPayload, CardGetAllEvent,
                                   CardCreatePayload, CardCreateEvent, CardLockEvent, CardLockPayload,
                                   CardUnlockPayload, CardUnlockEvent, CardChangeBalanceEvent, CardChangeBalancePayload,
                                   CardCheckPINEvent, CardCheckPINPayload, CardChangePINEvent, CardChangePINPayload,
                                   CardGetExtendedOnePayload, CardGetExtendedOneEvent)


class CardsGetOneUseCase(Protocol):
    def get_one(
        self, query: CardGetOnePayload
    ) -> CardGetOneEvent:
        ...


class CardsGetAllUseCase(Protocol):
    def get_all(
        self, query: CardGetAllPayload
    ) -> CardGetAllEvent:
        ...


class CardsIssueUseCase(Protocol):
    def issue(
        self, query: CardCreatePayload
    ) -> CardCreateEvent:
        ...


class CardsLockUseCase(Protocol):
    def lock(
        self, query: CardLockPayload
    ) -> CardLockEvent:
        ...


class CardsUnlockUseCase(Protocol):
    def unlock(
        self, query: CardUnlockPayload
    ) -> CardUnlockEvent:
        ...


class CardsChangeBalanceUseCase(Protocol):
    def change_balance(
        self, query: CardChangeBalancePayload
    ) -> CardChangeBalanceEvent:
        ...


class CardsCheckPINUseCase(Protocol):
    def check_pin(
        self, query: CardCheckPINPayload
    ) -> CardCheckPINEvent:
        ...


class CardsChangePINUseCase(Protocol):
    def change_pin(
        self, query: CardChangePINPayload
    ) -> CardChangePINEvent:
        ...


class CardsGetExtendedOneUseCase(Protocol):
    def get_extended_one(
        self, query: CardGetExtendedOnePayload
    ) -> CardGetExtendedOneEvent:
        ...
