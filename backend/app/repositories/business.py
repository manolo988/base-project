from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.business import Business
from ..schemas.business import BusinessCreate, BusinessUpdate
from .base import BaseRepository


class BusinessRepository(BaseRepository[Business, BusinessCreate, BusinessUpdate]):
    def __init__(self):
        super().__init__(Business)

    def create(self, db: Session, *, obj_in: BusinessCreate) -> Business:
        return super().create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: Business, obj_in: BusinessUpdate
    ) -> Business:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def get_by_email(self, db: Session, *, email: str) -> Optional[Business]:
        return db.query(Business).filter(Business.email == email).first()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Business]:
        return db.query(Business).filter(Business.id == id).first()


business_repository = BusinessRepository()
