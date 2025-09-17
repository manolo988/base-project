#!/usr/bin/env python3
"""Initialize the database with a superuser account."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Check if superuser exists
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()

    if not user:
        # Create superuser
        user = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            full_name="Admin User",
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        db.commit()
        print(f"Superuser created: {settings.FIRST_SUPERUSER_EMAIL}")
        print(f"Password: {settings.FIRST_SUPERUSER_PASSWORD}")
    else:
        print(f"Superuser already exists: {settings.FIRST_SUPERUSER_EMAIL}")

    db.close()

if __name__ == "__main__":
    init_db()