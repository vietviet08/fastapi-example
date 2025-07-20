"""
Database initialization module
"""
import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import engine, SessionLocal
from app.models.student import Student
from app.models.user import User
from app.services.auth_service import get_password_hash

logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables"""
    try:
        # Import all models to ensure they are registered with Base
        from app.models import student, user  # noqa
        
        # Create all tables
        from app.db.database import Base
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def check_database_connection():
    """Check if database connection is working"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def create_admin_user():
    """Create default admin user if not exists"""
    try:
        db: Session = SessionLocal()
        try:
            # Check if admin exists
            existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
            if existing_admin:
                logger.info("Admin user already exists")
                return
            
            # Create admin user
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_admin=True,
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            logger.info("Admin user created successfully (admin@example.com / admin123)")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        raise


def init_database():
    """Initialize database on application startup"""
    logger.info("Initializing database...")
    
    if not check_database_connection():
        raise Exception("Cannot connect to database")
    
    create_tables()
    create_admin_user()
    logger.info("Database initialization completed")
