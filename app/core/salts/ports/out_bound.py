from abc import ABC, abstractmethod

from app.core.salts.models import (SaltGetOnePayload, Salt, SaltAddPayload, SaltAddEvent, SaltGetOneEvent,
                                   SaltDeletePayload, SaltDeleteEvent)


class SaltDatabaseInterface(ABC):
    @abstractmethod
    def get_salt(
            self,
            payload: SaltGetOnePayload
    ) -> SaltGetOneEvent:
        ...

    @abstractmethod
    def add_salt(
            self,
            payload: SaltAddPayload
    ) -> SaltAddEvent:
        ...

    @abstractmethod
    def delete_salt(
            self,
            payload: SaltDeletePayload
    ) -> SaltDeleteEvent:
        ...
