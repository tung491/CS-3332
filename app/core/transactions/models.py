import uuid
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel


class Transaction(BaseModel):
    card_number: str
    debit_amount: float
    credit_amount: float
    pre_tx_balance: float
    post_tx_balance: float
    message: str
    timestamp: datetime
    user_id: str
    id: str = uuid.uuid4().hex


class TransactionResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    error_code: int = 200


class TransactionGetOnePayload(BaseModel):
    trx_id: str


class TransactionGetOneEvent(TransactionResponse):
    ...


class TransactionGetAllPayload(BaseModel):
    user_id: Optional[str]
    card_number: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TransactionGetAllEvent(BaseModel):
    transactions: List[Transaction]


class TransactionAddPayload(BaseModel):
    transaction: Transaction


class TransactionAddEvent(TransactionResponse):
    ...


class TransactionDeletePayload(BaseModel):
    trx_id: str


class TransactionDeleteEvent(TransactionResponse):
    ...
