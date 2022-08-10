import uuid
from typing import Optional, List

from flask_login import UserMixin
from pydantic import BaseModel


class Admin(BaseModel, UserMixin):
    id: Optional[str] = str(uuid.uuid4())
    email: str
    name: str
    password_hash: str


class AdminResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1
    data: Optional[Admin] = None


class AdminGetAllPayload(BaseModel):
    admin_id: Optional[str]
    email: Optional[str]
    name: Optional[str]


class AdminGetAllEvent(BaseModel):
    admins: List[Admin]


class AdminAddPayload(BaseModel):
    admin: Admin


class AdminAddEvent(AdminResponse):
    ...


class AdminDeletePayload(BaseModel):
    admin_id: str


class AdminDeleteEvent(BaseModel):
    data: dict


class AdminGetOnePayload(BaseModel):
    admin_id: Optional[str]
    email: Optional[str]


class AdminGetOneEvent(AdminResponse):
    ...


class AdminCreatePayload(BaseModel):
    admin: Admin


class AdminCreateEvent(AdminResponse):
    ...


class AdminCheckPasswordPayload(BaseModel):
    admin_id: str
    password: str


class AdminCheckPasswordEvent(BaseModel):
    match: bool
