from typing import Protocol

from app.core.admin.models import (AdminGetOneEvent, AdminGetOnePayload, AdminCheckPasswordPayload,
                                   AdminCheckPasswordEvent, AdminAddPayload, AdminAddEvent, AdminDeletePayload,
                                   AdminDeleteEvent)


class AdminsGetOneUseCase(Protocol):
    def get_one(
        self, query: AdminGetOnePayload
    ) -> AdminGetOneEvent:
        ...


class AdminsCheckPasswordUseCase(Protocol):
    def check_password(
        self, query: AdminCheckPasswordPayload
    ) -> AdminCheckPasswordEvent:
        ...


class AdminsGetAllUseCase(Protocol):
    def get_all(
        self, query: AdminGetOnePayload
    ) -> AdminGetOneEvent:
        ...


class AdminsAddUseCase(Protocol):
    def add_admin(
        self, query: AdminAddPayload
    ) -> AdminAddEvent:
        ...


class AdminsDeleteUseCase(Protocol):
    def delete_admin(
        self, query: AdminDeletePayload
    ) -> AdminDeleteEvent:
        ...
