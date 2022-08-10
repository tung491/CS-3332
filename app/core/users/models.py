import uuid
from datetime import datetime, date
from typing import Optional, List

from flask_login import UserMixin
from pydantic import BaseModel


class User(BaseModel, UserMixin):
    name: str
    id: Optional[str] = str(uuid.uuid4())
    date_of_birth: date
    email: str
    gender: str
    security_question: str
    security_answer: str


class UserResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1
    data: User


class UserGetOnePayload(BaseModel):
    user_id: str


class UserGetOneEvent(BaseModel):
    user: User


class UserGetAllPayload(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None


class UserGetAllEvent(BaseModel):
    users: List[User]


class UserCreatePayload(BaseModel):
    user: User


class UserCreateEvent(UserResponse):
    ...


class UserDeletePayload(BaseModel):
    user_id: str


class UserDeleteEvent(UserResponse):
    ...


class UserCheckSecurityAnswerPayload(BaseModel):
    user_id: str
    security_answer: str


class UserCheckSecurityAnswerEvent(BaseModel):
    match: bool


