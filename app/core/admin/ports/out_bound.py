from abc import ABC, abstractmethod

from app.core.admin.models import (AdminGetOneEvent, AdminGetOnePayload, AdminCheckPasswordEvent,
                                   AdminCheckPasswordPayload, AdminAddEvent, AdminAddPayload, AdminGetAllPayload,
                                   AdminGetAllEvent, AdminDeleteEvent, AdminDeletePayload)


class AdminDatabaseInterface(ABC):
    @abstractmethod
    def get_one(
            self,
            payload: AdminGetOnePayload
    ) -> AdminGetOneEvent:
        ...

    @abstractmethod
    def check_password(
            self,
            payload: AdminCheckPasswordPayload
    ) -> AdminCheckPasswordEvent:
        ...

    @abstractmethod
    def add_admin(
            self,
            payload: AdminAddPayload
    ) -> AdminAddEvent:
        ...

    @abstractmethod
    def get_all(
            self,
            payload: AdminGetAllPayload
    ) -> AdminGetAllEvent:
        ...

    @abstractmethod
    def delete_admin(
            self,
            payload: AdminDeletePayload
    ) -> AdminDeleteEvent:
        ...
