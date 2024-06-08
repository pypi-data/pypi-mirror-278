# type: ignore
import importlib.resources as resources
import logging
import os
import pathlib
from typing import Optional

from turbofan.database import Database

# https://realpython.com/python-logging/
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def migrate_database(database_path: Optional[pathlib.Path] = None) -> None:
    """
    Runs the SQL migrations to update the database schema.
    """
    logger.info("Bootstrapping database ...")
    directory_path = resources.files("profitpulse.migrations")
    db = Database(database_path)
    for file_name in directory_path.iterdir():
        if file_name.suffix == ".sql":
            logger.info(f"Running migration: {file_name} ...")
            file_path = os.path.join(directory_path, file_name)
            db.run_sql_file(file_path)
    logger.info("...done!")
