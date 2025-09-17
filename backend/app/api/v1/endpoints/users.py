from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....database import get_db
from ....repositories.user import user_repository
from ....schemas import user as user_schemas
from ....core.dependencies import get_current_active_user, get_current_superuser
from ....models.user import User

router = APIRouter()


@router.get("/", response_model=List[user_schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    users = user_repository.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=user_schemas.User)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return current_user


@router.put("/me", response_model=user_schemas.User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: user_schemas.UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    user = user_repository.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=user_schemas.User)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user


@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: user_schemas.UserUpdate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    user = user_repository.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = user_repository.update(db, db_obj=user, obj_in=user_in)
    return user