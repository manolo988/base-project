from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BusinessBase(BaseModel):
    email: str
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: str
    payment_information: dict


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    payment_information: Optional[dict] = None


class Business(BusinessBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
