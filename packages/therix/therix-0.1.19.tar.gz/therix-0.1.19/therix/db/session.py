# db/session.py

from sqlalchemy.orm import sessionmaker
from therix.db.db_manager import DatabaseManager

# Example PostgreSQL connection string
# Format: postgresql://user:password@hostname/database_name
db_manager = DatabaseManager()
SQLALCHEMY_DATABASE_URL = DatabaseManager._construct_db_url()

engine = DatabaseManager()._engine

engine.dispose()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
