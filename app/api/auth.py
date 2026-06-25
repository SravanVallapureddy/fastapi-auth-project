from fastapi import APIRouter, Depends
from sqlalchemy.orm import session

from app.schemas.user import UserCreate, UserLogin
from app.core.dependencies import get_db
from app.services.auth_service import create_user, get_user_by_email

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: session = Depends(get_db)):
    return get_user_by_email(db, user)

    
