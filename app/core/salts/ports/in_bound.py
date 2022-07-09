from typing import Protocol

from app.core.salts.models import (SaltGetOnePayload, SaltGetOneEvent, SaltAddEvent, SaltAddPayload, SaltDeletePayload,
                                   SaltDeleteEvent)


class SaltsGetOneUseCase(Protocol):
    def get_one(
        self, query: SaltGetOnePayload
    ) -> SaltGetOneEvent:
        ...


class SaltsAddUseCase(Protocol):
    def add(
        self, payload: SaltAddPayload
    ) -> SaltAddEvent:
        ...


class SaltsDeleteUseCase(Protocol):
    def delete(
        self, payload: SaltDeletePayload
    ) -> SaltDeleteEvent:
        ...
