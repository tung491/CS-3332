import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Transaction(BaseModel):
    debit_account_id: str
    credit_account_id: str
    withdrawal_amount: float
    deposit_amount: float
    pre_tx_balance: float
    post_tx_balance: float
    message: str
    date: datetime
    id: str = uuid.uuid4().hex


class TransactionResponse(BaseModel):
    success: bool
    message: str
    error_code: int
    data: dict


class TransactionGetOnePayload(BaseModel):
    trx_id: str


class TransactionGetOneEvent(TransactionResponse):
    ...


class TransactionGetAllPayload(BaseModel):
    debit_account_id: Optional[str] = None
    credit_account_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TransactionGetAllEvent(TransactionResponse):
    ...


class TransactionAddPayload(BaseModel):
    transaction: Transaction


class TransactionAddEvent(TransactionResponse):
    ...


class TransactionDeletePayload(BaseModel):
    trx_id: str


class TransactionDeleteEvent(TransactionResponse):
    ...
