from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse, UpdateProfileRequest, ChangePasswordRequest
from app.services.auth_service import (
    authenticate_user, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user
)
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Đăng nhập"""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_active_user)
):
    """Lấy thông tin user hiện tại"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.patch("/me", response_model=UserResponse)
async def update_user_profile(
    profile_data: UpdateProfileRequest,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cập nhật thông tin cá nhân người dùng"""
    user_service = UserService(db)
    updated_user = user_service.update_user_profile(current_user, profile_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        is_active=updated_user.is_active,
        is_admin=updated_user.is_admin,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_user_password(
    password_data: ChangePasswordRequest,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Thay đổi mật khẩu người dùng"""
    user_service = UserService(db)
    success = user_service.change_password(
        current_user, 
        password_data.current_password, 
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    return {"message": "Password changed successfully"}
