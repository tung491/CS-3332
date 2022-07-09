from app.core.salts.models import (SaltGetOnePayload, SaltGetOneEvent, SaltAddPayload, SaltAddEvent, SaltDeletePayload,
                                   SaltDeleteEvent)
from app.core.salts.ports.in_bound import SaltsGetOneUseCase, SaltsDeleteUseCase
from app.core.salts.ports.out_bound import SaltDatabaseInterface


class SaltsGetOneService(SaltsGetOneUseCase):
    def __init__(self, salt_db_interface: SaltDatabaseInterface):
        self.salt_db_interface = salt_db_interface

    def get_one(
            self, payload: SaltGetOnePayload
    ) -> SaltGetOneEvent:
        return self.salt_db_interface.get_salt(payload)


class SaltsAddService(SaltsGetOneUseCase):
    def __init__(self, salt_db_interface: SaltDatabaseInterface):
        self.salt_db_interface = salt_db_interface

    def add(
            self, payload: SaltAddPayload
    ) -> SaltAddEvent:
        return self.salt_db_interface.add_salt(payload)


class SaltsDeleteService(SaltsDeleteUseCase):
    def __init__(self, salt_db_interface: SaltDatabaseInterface):
        self.salt_db_interface = salt_db_interface

    def delete(
            self, payload: SaltDeletePayload
    ) -> SaltDeleteEvent:
        return self.salt_db_interface.delete_salt(payload)
