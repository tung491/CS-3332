from abc import ABC, abstractmethod

from app.core.users.models import (UserGetOnePayload, UserGetOneEvent, UserGetAllPayload, UserGetAllEvent,
                                   UserCreatePayload, UserCreateEvent, UserCheckSecurityAnswerPayload,
                                   UserCheckSecurityAnswerEvent, UserDeletePayload, UserDeleteEvent)


class UserDatabaseInterface(ABC):
    @abstractmethod
    def get_one(
            self,
            payload: UserGetOnePayload
    ) -> UserGetOneEvent:
        ...

    @abstractmethod
    def get_all(
            self,
            payload: UserGetAllPayload
    ) -> UserGetAllEvent:
        ...

    @abstractmethod
    def add_user(
            self,
            payload: UserCreatePayload
    ) -> UserCreateEvent:
        ...

    @abstractmethod
    def delete_user(
            self,
            payload: UserDeletePayload
    ) -> UserDeleteEvent:
        ...

    @abstractmethod
    def check_security_answer(
            self,
            payload: UserCheckSecurityAnswerPayload
    ) -> UserCheckSecurityAnswerEvent:
        ...
