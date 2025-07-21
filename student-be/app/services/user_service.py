from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate, UpdateProfileRequest
from app.services.auth_service import get_password_hash, verify_password


class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_create: UserCreate, is_admin: bool = False) -> User:
        """Tạo user mới"""
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_email(self, email: str) -> User:
        """Lấy user theo email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def user_exists(self, email: str) -> bool:
        """Kiểm tra user có tồn tại không"""
        return self.db.query(User).filter(User.email == email).first() is not None
    
    def update_user_profile(self, user: User, update_data: UpdateProfileRequest) -> User:
        """Cập nhật thông tin user"""
        if update_data.email is not None:
            # Check if email already exists
            existing_user = self.get_user_by_email(update_data.email)
            if existing_user and existing_user.id != user.id:
                return None
            user.email = update_data.email
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def change_password(self, user: User, current_password: str, new_password: str) -> bool:
        """Đổi mật khẩu"""
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            return False
        
        # Hash and set new password
        user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True
