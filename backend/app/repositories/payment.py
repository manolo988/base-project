from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.payment import Payment
from ..schemas.payment import PaymentCreate, PaymentUpdate
from .base import BaseRepository


class PaymentRepository(BaseRepository[Payment, PaymentCreate, PaymentUpdate]):
    def __init__(self):
        super().__init__(Payment)

    def create_payment(self, db: Session, *, obj_in: PaymentCreate) -> Payment:
        return super().create(db, obj_in=obj_in)

    def update_payment(
        self, db: Session, *, db_obj: Payment, obj_in: PaymentUpdate
    ) -> Payment:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def get_payment_by_id(self, db: Session, *, id: int) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == id).first()

    def get_payment_by_business_id(
        self, db: Session, *, business_id: int
    ) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.business_id == business_id).first()

    def get_payments(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Payment]:
        return (
            db.query(Payment)
            .filter(Payment.status == status)
            .order_by(Payment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


payment_repository = PaymentRepository()
