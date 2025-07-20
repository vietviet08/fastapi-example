from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate
from app.services.auth_service import get_password_hash


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
