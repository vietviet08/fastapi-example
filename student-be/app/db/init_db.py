"""
Database initialization module
"""
import logging
from sqlalchemy import text
from app.db.database import engine
from app.models.student import Student

logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables"""
    try:
        # Import all models to ensure they are registered with Base
        from app.models import student  # noqa
        
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


def init_database():
    """Initialize database on application startup"""
    logger.info("Initializing database...")
    
    if not check_database_connection():
        raise Exception("Cannot connect to database")
    
    create_tables()
    logger.info("Database initialization completed")
