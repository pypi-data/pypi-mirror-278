from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from alembic.config import Config
from alembic import command
import threading
import logging
import os

from therix.entities.models import Base


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        logger.debug("Checking instance...")
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    logger.debug("Creating new instance...")
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._engine = cls._create_engine()
                    cls._session_factory = sessionmaker(
                        bind=cls._engine, autoflush=False, autocommit=False
                    )
                    cls._setup_database()
        return cls._instance

    @classmethod
    def get_session(cls):
        if cls._session_factory is None:
            raise Exception("DatabaseManager is not initialized properly.")
        return scoped_session(cls._session_factory)

    @classmethod
    def _create_engine(cls):
        db_url = cls._construct_db_url()
        return create_engine(db_url)

    @classmethod
    def _construct_db_url(cls):
        drivername = os.getenv("THERIX_DB_TYPE", "postgresql")
        username = os.getenv("THERIX_DB_USERNAME")
        password = os.getenv("THERIX_DB_PASSWORD")
        host = os.getenv("THERIX_DB_HOST")
        port = os.getenv("THERIX_DB_PORT")
        db_name = os.getenv("THERIX_DB_NAME")
        return URL.create(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=db_name,
        ).render_as_string(hide_password=False)

    @staticmethod
    def _setup_database():
        # Placeholder for database setup logic like migrations

        Base.metadata.create_all(DatabaseManager._engine)
        logger.info("Database tables created.")

        alembic_cfg = DatabaseManager._get_alembic_config()
        DatabaseManager._upgrade_database(alembic_cfg)

    @staticmethod
    def _get_alembic_config():
        # Navigate up two levels from the current file location to find the Alembic directory.
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        alembic_config_path = os.path.join(base_dir, "therix/alembic.ini")
        alembic_cfg = Config(alembic_config_path)
        alembic_cfg.set_main_option(
            "script_location", os.path.join(base_dir, "therix/alembic")
        )
        alembic_cfg.set_main_option(
            "sqlalchemy.url", str(DatabaseManager._construct_db_url())
        )
        return alembic_cfg

    @staticmethod
    def _upgrade_database(alembic_cfg):
        try:
            # command.upgrade(alembic_cfg, "head")
            # logger.info("Database upgraded successfully.")
            pass
        except Exception as e:
            logger.error(f"An error occurred while upgrading the database: {e}")
            raise


# Unit testing with pytest will be created next. This would involve testing these functionalities effectively.


db_manager = DatabaseManager()
# Example usage:
# db_manager = DatabaseManager(
#     "postgresql", "postgres", "password", "localhost", "5432", "coditas_dot_ai"
# )
# db_manager1 = DatabaseManager()
# session = db_manager.create_session()
# # Use the session for ORM operations
# db_manager.test_connection()
# session.close()
