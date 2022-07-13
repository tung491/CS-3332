from enum import Enum
from typing import Optional, List

from flask_login import UserMixin
from pydantic import BaseModel

from app.core.users.models import User


class SortEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class Card(BaseModel):
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
    card_number: int


class CardGetOneEvent(CardResponse):
    ...


class CardCreatePayload(BaseModel):
    card: Card


class CardCreateEvent(CardResponse):
    ...


class CardGetAllPayload(BaseModel):
    user_id: Optional[str] = None
    card_type: Optional[str] = None


class CardGetAllEvent(BaseModel):
    data: List[Card]


class CardLockPayload(BaseModel):
    number: int


class CardLockEvent(CardResponse):
    ...


class CardUnlockPayload(BaseModel):
    number: int


class CardUnlockEvent(CardResponse):
    ...


class   CardChangeBalancePayload(BaseModel):
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


class CardChangePINEvent(CardResponse):
    ...


class CardGetExtendedOnePayload(BaseModel):
    card_number: int


class CardGetExtendedOneEvent(ExtendedCardResponse):
    ...
