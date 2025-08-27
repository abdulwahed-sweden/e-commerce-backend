"""
Authentication routes for user registration, login, and token management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import schemas, models
from .database import get_db
from .auth_utils import (
    authenticate_user, 
    create_tokens_for_user, 
    store_refresh_token,
    validate_refresh_token,
    invalidate_refresh_token,
    get_password_hash,
    validate_password_strength,
    verify_token
)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=schemas.User)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Validate password strength
    is_valid, message = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Create new user
    try:
        hashed_password = get_password_hash(user_data.password)
        db_user = models.User(
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    User login - returns JWT tokens
    """
    # Authenticate user
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )
    
    # Create tokens
    tokens = create_tokens_for_user(user)
    
    # Store refresh token in database
    store_refresh_token(db, user.id, tokens["refresh_token"])
    
    return tokens

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    refresh_data: schemas.RefreshTokenRequest, 
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    # Verify refresh token format
    token_data = verify_token(refresh_data.refresh_token, token_type="refresh")
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate refresh token in database
    user = validate_refresh_token(db, refresh_data.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )
    
    # Create new tokens
    tokens = create_tokens_for_user(user)
    
    # Store new refresh token and invalidate old one
    invalidate_refresh_token(db, refresh_data.refresh_token)
    store_refresh_token(db, user.id, tokens["refresh_token"])
    
    return tokens

@router.post("/logout")
async def logout(
    refresh_data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Logout user by invalidating refresh token
    """
    success = invalidate_refresh_token(db, refresh_data.refresh_token)
    if success:
        return {"message": "Successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )

