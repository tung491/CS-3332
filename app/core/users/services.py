from app.core.users.models import (UserGetOnePayload, UserGetOneEvent, UserGetAllPayload, UserGetAllEvent,
                                   UserDeletePayload, UserDeleteEvent, UserCreatePayload, UserCreateEvent,
                                   UserCheckSecurityAnswerPayload, UserCheckSecurityAnswerEvent)
from app.core.users.ports.in_bound import (UserGetOneUseCase, UserGetAllUseCase, UserCreateUseCase, UserDeleteUseCase,
                                           UserCheckSecurityAnswerUseCase)
from app.core.users.ports.out_bound import UserDatabaseInterface


class UsersGetOneService(UserGetOneUseCase):
    def __init__(self, user_db_interface: UserDatabaseInterface):
        self.user_db_interface = user_db_interface

    def get_one(self, payload: UserGetOnePayload) -> UserGetOneEvent:
        try:
            resp = self.user_db_interface.get_one(payload)
        except Exception as e:
            raise e
        return resp


class UsersGetAllService(UserGetAllUseCase):
    def __init__(self, user_db_interface: UserDatabaseInterface):
        self.user_db_interface = user_db_interface

    def get_all(self, payload: UserGetAllPayload) -> UserGetAllEvent:
        try:
            resp = self.user_db_interface.get_all(payload)
        except Exception as e:
            raise e
        return resp


class UsersCreateService(UserCreateUseCase):
    def __init__(self, user_db_interface: UserDatabaseInterface):
        self.user_db_interface = user_db_interface

    def create(self, payload: UserCreatePayload) -> UserCreateEvent:
        try:
            user = self.user_db_interface.add_user(payload)
        except Exception as e:
            raise e
        return UserGetOneEvent(user=payload.user)


class UsersDeleteService(UserDeleteUseCase):
    def __init__(self, user_db_interface: UserDatabaseInterface):
        self.user_db_interface = user_db_interface

    def delete(self, payload: UserDeletePayload) -> UserDeleteEvent:
        try:
            user = self.user_db_interface.delete_user(payload)
        except Exception as e:
            raise e
        return UserDeleteEvent()


class UsersCheckSecurityAnswerService(UserCheckSecurityAnswerUseCase):
    def __init__(self, user_db_interface: UserDatabaseInterface):
        self.user_db_interface = user_db_interface

    def check_security_answer(self, payload: UserCheckSecurityAnswerPayload) -> UserCheckSecurityAnswerEvent:
        try:
            resp = self.user_db_interface.check_security_answer(payload)
        except Exception as e:
            raise e
        return resp
