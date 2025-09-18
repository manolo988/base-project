from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....database import get_db
from ....repositories.payment import payment_repository
from ....schemas import payment as payment_schemas
from ....models.payment import Payment

router = APIRouter()


@router.post("/", response_model=payment_schemas.Payment)
def create_payment(
    *,
    db: Session = Depends(get_db),
    payment_in: payment_schemas.PaymentCreate,
) -> Any:
    payment = payment_repository.create_payment(db, obj_in=payment_in)
    return payment
