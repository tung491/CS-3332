from typing import Protocol

from app.core.users.models import (UserGetOnePayload, UserGetAllPayload, UserGetAllEvent, UserGetOneEvent,
                                   UserDeletePayload, UserDeleteEvent, UserCreatePayload, UserCreateEvent,
                                   UserCheckSecurityAnswerPayload, UserCheckSecurityAnswerEvent)


class UserGetOneUseCase(Protocol):
    def get_one(
            self,
            payload: UserGetOnePayload
            ) -> UserGetOneEvent:
        ...


class UserGetAllUseCase(Protocol):
    def get_all(
            self,
            payload: UserGetAllPayload
            ) -> UserGetAllEvent:
        ...


class UserCreateUseCase(Protocol):
    def create(
            self,
            payload: UserCreatePayload
            ) -> UserCreateEvent:
        ...


class UserDeleteUseCase(Protocol):
    def delete(
            self,
            payload: UserDeletePayload
            ) -> UserDeleteEvent:
        ...


class UserCheckSecurityAnswerUseCase(Protocol):
    def check_security_answer(
            self,
            payload: UserCheckSecurityAnswerPayload
            ) -> UserCheckSecurityAnswerEvent:
        ...
