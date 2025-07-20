from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.services.auth_service import get_password_hash


def create_admin_user():
    """Tạo tài khoản admin mặc định"""
    # Tạo tất cả bảng
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Kiểm tra xem admin đã tồn tại chưa
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Tạo admin user
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"Admin user created successfully!")
        print(f"Email: {admin_user.email}")
        print(f"Password: admin123")
        print(f"Is Admin: {admin_user.is_admin}")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
