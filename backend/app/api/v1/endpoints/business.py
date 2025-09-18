from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....database import get_db
from ....repositories.business import business_repository
from ....schemas import business as business_schemas
from ....models.business import Business

router = APIRouter()


@router.post("/", response_model=business_schemas.Business)
def create_business(
    *,
    db: Session = Depends(get_db),
    business_in: business_schemas.BusinessCreate,
) -> Any:
    business = business_repository.create(db, obj_in=business_in)
    return business
