from app.adapters.database.postgres import PostgresUserAdapter
from app.core.users.models import UserGetOneEvent, UserGetOnePayload, UserGetAllPayload, UserGetAllEvent
from app.core.users.ports.out_bound import UserDatabaseInterface
from app.core.users.services import (UsersGetOneService, UsersGetAllService, UsersCreateService, UsersDeleteService,
                                     UsersCheckSecurityAnswerService)
from app.settings import get_app_settings


def user_interface() -> PostgresUserAdapter:
    return PostgresUserAdapter()


def user_get_one_service(
        user_db_interface: UserDatabaseInterface,
) -> UsersGetOneService:
    return UsersGetOneService(user_db_interface)


def user_get_all_service(
        user_db_interface: UserDatabaseInterface,
) -> UsersGetAllService:
    return UsersGetAllService(user_db_interface)


def user_create_service(
        user_db_interface: UserDatabaseInterface,
) -> UsersCreateService:
    return UsersCreateService(user_db_interface)


def user_delete_service(
        user_db_interface: UserDatabaseInterface,
) -> UsersDeleteService:
    return UsersDeleteService(user_db_interface)


def user_check_security_answer_service(
        user_db_interface: UserDatabaseInterface,
) -> UsersCheckSecurityAnswerService:
    return UsersCheckSecurityAnswerService(user_db_interface)
