from fastapi import HTTPException

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.schemas.user import UserResponse

def create_user(db, user_data):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = User(
        full_name = user_data.full_name,
        email = user_data.email,
        password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"New user created: {new_user.full_name} ({new_user.email})")
    
    return UserResponse.model_validate(new_user)

def get_user_by_email(db, user_data):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    password_matches = verify_password(user_data.password, db_user.password)
    
    if not password_matches:
        raise HTTPException(status_code=400, detail="Invalid password")

    return db_user