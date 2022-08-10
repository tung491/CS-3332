from app.core.admin.models import (AdminGetOnePayload, AdminGetOneEvent, AdminCheckPasswordPayload,
                                   AdminCheckPasswordEvent, AdminAddPayload, AdminAddEvent, AdminGetAllPayload,
                                   AdminGetAllEvent, AdminDeleteEvent, AdminDeletePayload)
from app.core.admin.ports.in_bound import AdminsGetOneUseCase, AdminsGetAllUseCase, AdminsDeleteUseCase
from app.core.admin.ports.out_bound import AdminDatabaseInterface


class AdminsGetOneService(AdminsGetOneUseCase):
    def __init__(self, admin_db_interface: AdminDatabaseInterface):
        self.admin_db_interface = admin_db_interface

    def get_one(
            self, payload: AdminGetOnePayload
    ) -> AdminGetOneEvent:
        return self.admin_db_interface.get_one(payload)


class AdminsGetAllService(AdminsGetAllUseCase):
    def __init__(self, admin_db_interface: AdminDatabaseInterface):
        self.admin_db_interface = admin_db_interface

    def get_all(
            self, payload: AdminGetAllPayload
    ) -> AdminGetAllEvent:
        return self.admin_db_interface.get_all(payload)


class AdminsAddService(AdminsGetOneUseCase):
    def __init__(self, admin_db_interface: AdminDatabaseInterface):
        self.admin_db_interface = admin_db_interface

    def add_admin(
            self, payload: AdminAddPayload
    ) -> AdminAddEvent:
        return self.admin_db_interface.add_admin(payload)


class AdminsCheckPasswordService(AdminsGetOneUseCase):
    def __init__(self, admin_db_interface: AdminDatabaseInterface):
        self.admin_db_interface = admin_db_interface

    def check_password(
            self, payload: AdminCheckPasswordPayload
    ) -> AdminCheckPasswordEvent:
        return self.admin_db_interface.check_password(payload)


class AdminsDeleteService(AdminsDeleteUseCase):
    def __init__(self, admin_db_interface: AdminDatabaseInterface):
        self.admin_db_interface = admin_db_interface

    def delete_admin(
            self, payload: AdminDeletePayload
    ) -> AdminDeleteEvent:
        return self.admin_db_interface.delete_admin(payload)
