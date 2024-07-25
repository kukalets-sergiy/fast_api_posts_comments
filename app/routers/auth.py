from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from app import crud
from app.config import JWT_SECRET_KEY
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse


router = APIRouter()
access_security = JwtAccessBearer(secret_key=JWT_SECRET_KEY)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or db_user.hashed_password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_active": db_user.is_active
    }

    access_token = access_security.create_access_token(subject=token_data)
    return {"access_token": access_token}


@router.get("/users/me", response_model=UserResponse)
def read_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return {
            "id": credentials["id"],
            "username": credentials["username"],
            "email": credentials["email"],
            "is_active": credentials["is_active"],
            }
