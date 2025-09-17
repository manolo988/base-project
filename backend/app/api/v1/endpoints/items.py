from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ....database import get_db
from ....repositories.item import item_repository
from ....schemas import item as item_schemas
from ....schemas.common import PaginatedResponse
from ....core.dependencies import get_current_active_user
from ....models.user import User
import math

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[item_schemas.Item])
def read_items(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    skip = (page - 1) * page_size
    items = item_repository.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=page_size
    )
    total = db.query(item_repository.model).filter_by(owner_id=current_user.id).count()
    pages = math.ceil(total / page_size)

    return PaginatedResponse[item_schemas.Item](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.post("/", response_model=item_schemas.Item)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: item_schemas.ItemCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    item = item_repository.create_with_owner(
        db, obj_in=item_in, owner_id=current_user.id
    )
    return item


@router.get("/{item_id}", response_model=item_schemas.Item)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    item = item_repository.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item


@router.put("/{item_id}", response_model=item_schemas.Item)
def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: item_schemas.ItemUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    item = item_repository.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = item_repository.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}", response_model=item_schemas.Item)
def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    item = item_repository.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = item_repository.remove(db, id=item_id)
    return item