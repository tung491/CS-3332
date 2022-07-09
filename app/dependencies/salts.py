from app.adapters.database.postgres import PostgresSaltAdapter
from app.core.salts.services import SaltsGetOneService, SaltsAddService, SaltsDeleteService


def salt_interface() -> PostgresSaltAdapter:
    return PostgresSaltAdapter()


def salt_get_one_service(
        salt_db_interface: PostgresSaltAdapter,
) -> SaltsGetOneService:
    return SaltsGetOneService(salt_db_interface)


def salt_add_service(
        salt_db_interface: PostgresSaltAdapter,
) -> SaltsAddService:
    return SaltsAddService(salt_db_interface)


def salt_delete_service(
        salt_db_interface: PostgresSaltAdapter,
) -> SaltsDeleteService:
    return SaltsDeleteService(salt_db_interface)
