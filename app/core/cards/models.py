import uuid
from enum import Enum
from typing import Optional, List

from flask_login import UserMixin
from pydantic import BaseModel

from app.core.users.models import User


class SortEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class Card(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    number: int
    user_id: str
    pin: str
    type: str
    locked: bool
    balance: float


class ExtendedCard(Card, UserMixin):
    id: Optional[str] = None
    user: User


class CardResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1
    data: Optional[Card]


class ExtendedCardResponse(CardResponse):
    data: Optional[ExtendedCard]


class CardGetOnePayload(BaseModel):
    card_number: Optional[int]
    card_id: Optional[str]


class CardGetOneEvent(CardResponse):
    ...


class CardCreatePayload(BaseModel):
    card: Card


class CardCreateEvent(CardResponse):
    ...


class CardGetAllPayload(BaseModel):
    card_id: Optional[str]
    card_number: Optional[int]
    user_id: Optional[str]
    card_type: Optional[str]
    locked: Optional[bool]


class CardGetAllEvent(BaseModel):
    data: List[Card]


class CardLockPayload(BaseModel):
    number: int


class CardLockEvent(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1


class CardUnlockPayload(BaseModel):
    number: int


class CardUnlockEvent(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1


class CardChangeBalancePayload(BaseModel):
    number: int
    balance: float


class CardChangeBalanceEvent(CardResponse):
    data: dict


class CardCheckPINPayload(BaseModel):
    number: int
    pin_hash: str


class CardCheckPINEvent(BaseModel):
    match: bool


class CardChangePINPayload(BaseModel):
    number: int
    pin_hash: str


class CardChangePINEvent(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = -1


class CardGetExtendedOnePayload(BaseModel):
    card_number: int


class CardGetExtendedOneEvent(ExtendedCardResponse):
    ...
