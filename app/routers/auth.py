from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud
from app.config import settings
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()
access_security = JwtAccessBearer(secret_key=settings.secret_key, auto_error=True)


@router.post("/register", response_model=UserResponse)
async def register(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    # Check if the email is already registered
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create and return the new user
    return await crud.create_user(db=db, user=user)


@router.get("/", response_model=List[UserResponse])
async def read_users(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    # Fetch users from the database
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/login")
async def login(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    # Fetch the user by email
    db_user = await crud.get_user_by_email(db, email=user.email)
    if not db_user or db_user.hashed_password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create and return access token
    token_data = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_active": db_user.is_active
    }
    access_token = access_security.create_access_token(subject=token_data)
    return {"access_token": access_token}


@router.get("/users/me", response_model=UserResponse)
async def read_current_user(
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return {
        "id": credentials["id"],
        "username": credentials["username"],
        "email": credentials["email"],
        "is_active": credentials["is_active"],
    }
