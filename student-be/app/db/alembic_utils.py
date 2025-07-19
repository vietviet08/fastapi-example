"""
Alembic migration utilities for automatic database initialization
"""
import subprocess
import os
import logging

logger = logging.getLogger(__name__)


def run_alembic_migration():
    """Run Alembic upgrade to create/update database tables"""
    try:
        # Get the project root directory (where alembic.ini is located)
        current_dir = os.path.dirname(__file__)  # app/db
        project_root = os.path.dirname(os.path.dirname(current_dir))  # Go up to project root
        
        # Change to project root directory and run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info("Database migration completed successfully")
        logger.info(f"Alembic output: {result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("Alembic not found. Please install alembic: pip install alembic")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return False


def check_alembic_current():
    """Check current Alembic migration version"""
    try:
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        result = subprocess.run(
            ["alembic", "current"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"Current migration: {result.stdout.strip()}")
        return result.stdout.strip()
        
    except Exception as e:
        logger.error(f"Error checking current migration: {e}")
        return None


def init_database_with_alembic():
    """Initialize database using Alembic migrations"""
    logger.info("Initializing database with Alembic...")
    
    # Check current migration state
    current = check_alembic_current()
    
    if not current or "(head)" not in current:
        logger.info("Running Alembic migration...")
        if run_alembic_migration():
            logger.info("Database initialization with Alembic completed successfully")
        else:
            logger.error("Database initialization with Alembic failed")
            raise Exception("Failed to initialize database with Alembic")
    else:
        logger.info("Database is already up to date")
