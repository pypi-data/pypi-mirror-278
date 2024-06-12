import logging
import uuid
from typing import Optional

from orcalib.database import OrcaDatabase, TableHandle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TemporaryDatabase:
    """
    A context manager for creating and dropping temporary databases.

    Args:
        db_name (Optional[str]): The name of the temporary database. If not provided, a random name will be generated.
        verbose (bool): Whether to log verbose information about the creation and dropping of the temporary database.

    Returns:
        OrcaDatabase: The temporary database object.

    Example:

    .. code-block:: python

        with TemporaryDatabase(db_name="my_temp_db", verbose=True) as temp_db:
            # Use the temporary database
            ...
    """

    def __init__(self, db_name: Optional[str] = None, verbose: bool = False) -> None:
        """
        :param db_name: The name of the temporary database. If not provided, a random name will be generated. (default: None)
        :param verbose: Whether to log verbose information about the creation and dropping of the temporary database. (default: False)
        """
        if db_name is None:
            self.db_name = "temp_db_" + str(uuid.uuid4()).replace("-", "_")
        else:
            self.db_name = db_name

        self.verbose = verbose

    def __enter__(self) -> OrcaDatabase:
        """
        Create the temporary database and return the database object.
        """
        if self.verbose:
            logger.info(f"Creating temporary database: {self.db_name}")

        self.db = OrcaDatabase(self.db_name)
        return self.db

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Drop the temporary database.

        :param exc_type: The type of the exception
        :param exc_value: The exception value
        :param traceback: The traceback
        """
        if self.verbose:
            logger.info(f"Dropping temporary database: {self.db_name}")

        OrcaDatabase.drop_database(self.db_name)


class TemporaryTable:
    """
    A context manager for creating and dropping temporary tables in a database.

    Args:
        db (OrcaDatabase): The database object where the temporary table will be created.
        table_name (str, optional): The name of the temporary table. If not provided, a unique name will be generated.
        verbose (bool, optional): Whether to log information about creating and dropping the temporary table.
        **kwargs: Additional keyword arguments to be passed to the `create_table` method of the database.

    Returns:
        TableHandle: The handle to the created temporary table.

    Example:

    .. code-block:: python

        with TemporaryTable(db, table_name="my_temp_table", verbose=True, columns=["id INT", "name TEXT"]) as table:
            # Use the temporary table within this block
            ...
    """

    def __init__(self, db: OrcaDatabase, table_name: Optional[str] = None, verbose: bool = False, **kwargs):
        """
        :param db: The database object where the temporary table will be created.
        :param table_name: The name of the temporary table. If not provided, a unique name will be generated.
        :param verbose: Whether to log information about creating and dropping the temporary table.
        :param kwargs: Additional keyword arguments to be passed to the `create_table` method of the database.
        """
        self.db = db
        self.verbose = verbose

        if table_name is None:
            self.table_name = "temp_table_" + str(uuid.uuid4()).replace("-", "_")
        else:
            self.table_name = table_name

        self.kwargs = kwargs

    def __enter__(self) -> TableHandle:
        """Create the temporary table and return the table handle.

        :return: TableHandle
        """
        if self.verbose:
            logger.info(f"Creating temporary table: {self.table_name} in database {self.db.name}")

        self.table = self.db.create_table(self.table_name, **self.kwargs)
        return self.table

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Drop the temporary table.

        :param exc_type: The type of the exception
        :param exc_value: The exception value
        :param traceback: The traceback
        """
        if self.verbose:
            logger.info(f"Dropping temporary table: {self.table_name} in database {self.db.name}")

        self.db.drop_table(self.table_name, error_if_not_exists=False)
