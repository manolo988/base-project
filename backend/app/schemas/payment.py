from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PaymentBase(BaseModel):
    business_id: int
    user_id: Optional[int] = None
    order_id: str
    amount: int
    accepted_payment_types: Optional[str] = None
    expires_at: Optional[datetime] = None
    status: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    business_id: Optional[int] = None
    user_id: Optional[int] = None
    order_id: Optional[str] = None
    amount: Optional[int] = None
    accepted_payment_types: Optional[str] = None
    expires_at: Optional[datetime] = None
    status: Optional[str] = None


class Payment(PaymentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
