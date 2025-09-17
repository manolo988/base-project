from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    order_id = Column(String, nullable=False)
    amount = Column(BigInteger, nullable=False)  # in cents
    accepted_payment_types = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)  # pending, approved, rejected, expired
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
