from dataclasses import dataclass
from datetime import datetime
from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel


class Salt(BaseModel):
    user_id: str
    salt: str


class SaltResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1
    data: Salt


class SaltGetOnePayload(BaseModel):
    user_id: str


class SaltGetOneEvent(Salt):
    ...


class SaltAddPayload(BaseModel):
    user_id: str


class SaltAddEvent(BaseModel):
    ...


class SaltDeletePayload(BaseModel):
    user_id: str


class SaltDeleteEvent(SaltResponse):
    ...
