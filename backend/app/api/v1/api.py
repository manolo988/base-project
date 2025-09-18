from fastapi import APIRouter
from .endpoints import auth, items, users, payment, business

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(payment.router, prefix="/payment", tags=["payment"])
api_router.include_router(business.router, prefix="/business", tags=["business"])
