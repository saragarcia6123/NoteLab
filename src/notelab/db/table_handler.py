import logging
import sqlite3
from typing import Any, Dict, List, Optional, Tuple
from .connection_handler import ConnectionHandler

class TableHandler:

    def __init__(self, logger: logging.Logger, db_name: str, messages: dict, connection_handler: ConnectionHandler):
        self.logger = logger
        self.MESSAGES = messages
        self.db_name = db_name
        self.connection_handler = connection_handler

    def connected(self) -> bool:
        return self.connection_handler.connected

    def cursor(self) -> sqlite3.Cursor:
        return self.connection_handler.cursor

    def db(self) -> sqlite3.Connection:
        return self.connection_handler.db

    """
    Check if table exists
    Parameters:
        table_name (str) - The name of the table to check
    Returns:
        True if table exists, False otherwise
    """
    def table_exists(self, table_name: str) -> bool:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True, force=True)
            if status is not None:
                return False

            query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
            self.cursor().execute(query, (table_name,))
            self.logger.info(f"Checking if table {table_name} exists in database {self.db_name}...")
            exists = self.cursor().fetchone() is not None
            if exists:
                status = 200
                message = self.MESSAGES["TABLE_FOUND"].format(table_name=table_name)
                self.logger.info(f"{message}, {status}")
                return True
            else:
                status = 404
                message = self.MESSAGES["TABLE_NOT_FOUND"].format(table_name=table_name)
                self.logger.warning(f"{message}, {status}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to check if table {table_name} exists: {str(e)}")
            return False

    """
    Validate table status before creating or deleting
    Parameters:
        table_name (str) - The name of the table to validate
        exist_condition (bool) - Whether the table should exist or not
        force (bool) - Whether to force validation
    Returns:
        - Message (str)
        - HTTP Status Code (int)
    """
    def validate_table_status(self, table_name: str, exist_condition: bool, force: bool = False) -> Optional[Tuple[str, int]]:
        if not self.connected():
            message = self.MESSAGES["NOT_CONNECTED"]
            status = 400
            self.logger.warning(f"{message}, {status}")
            return message, status

        if force:
            return None

        table_exists = self.table_exists(table_name)

        if table_exists and exist_condition == False:
            message = self.MESSAGES["TABLE_EXISTS"].format(table_name=table_name)
            status = 409
            self.logger.warning(f"{message}, {status}")
            return message, status

        if not table_exists and exist_condition == True:
            message = self.MESSAGES["TABLE_NOT_FOUND"].format(table_name=table_name)
            status = 404
            self.logger.warning(f"{message}, {status}")
            return message, status

        return None

    """
    Retrieve table from SQLite Database
    Parameters:
    table_name - The name of the table to retrieve
    Returns:
        - A list of dictionaries representing the rows of the table if found,
          None otherwise
        - HTTP Status Code (int)
    """
    def get_table(self, table_name: str) -> Tuple[Optional[List[dict]], int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return None, status[1]

            query = f"SELECT * FROM {table_name}"
            self.cursor().execute(query)
            rows = self.cursor().fetchall()

            if not rows:
                message = self.MESSAGES["ROWS_NOT_FOUND"].format(table_name=table_name)
                status = 200
                self.logger.info(f"{message}, {status}")
                return [], status

            columns = [column[0] for column in self.cursor().description]
            result = [dict(zip(columns, row)) for row in rows]

            message = self.MESSAGES["TABLE_RETRIEVED"].format(table_name=table_name)
            status = 200
            self.logger.info(f"{message}, {status}")
            return result, status

        except sqlite3.Error as e:
            message = f"Database error occurred while retrieving table {table_name}: {str(e)}"
            status = 500
            self.logger.error(f"{message}, {status}")
            return None, status

        except Exception as e:
            message = f"Unexpected error occurred while retrieving table {table_name}: {str(e)}"
            status = 500
            self.logger.error(f"{message}, {status}")
            return None, status

    """
    Retrieves all table data from SQLite Database
    Returns:
        - A dictionary with the names of the tables as keys. Each value is another dictionary containing:
            - "columns": list of str, the names of the columns.
            - "rows": list of tuples, where each tuple represents a row of data from the table.
            Otherwise None If the database is not connected, or if there are no tables, or if an error occurs during retrieval.
        - HTTP Status Code (int)
    """
    def get_tables(self) -> Tuple[Optional[Dict[str, Dict[str, Any]]], int]:
        try:
            if not self.connected:
                self.logger.info(self.MESSAGES["NOT_CONNECTED"])
                return None, 400

            query = "SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';"
            self.cursor().execute(query)
            table_names = self.cursor().fetchall()

            if not table_names:
                self.logger.info(self.MESSAGES["NO_TABLES_FOUND"])
                return {"tables": {}}, 200

            all_table_data = {}

            for table_name in table_names:
                table_name = table_name[0]
                # Ensure the table_name is safe to use directly in a query
                query = f"SELECT * FROM {table_name}"

                # Execute query without additional bindings since no parameters are required
                self.cursor().execute(query)
                rows = self.cursor().fetchall()
                column_names = [description[0] for description in self.cursor().description]
                table_data = {
                    "columns": column_names,
                    "rows": rows
                }
                self.logger.info(f"Table {table_name} data retrieved.")
                all_table_data[table_name] = table_data

            self.logger.info("All table data retrieved.")
            return {"tables": all_table_data}, 200

        except Exception as e:
            self.logger.error(f"Unexpected error occurred while retrieving all table data: {str(e)}")
            return None, 500

    """
    Retrieves the schema of a specified table within the connected SQLite database.
    Parameters:
        - table_name (str) - The name of the table whose schema is to be retrieved
    Returns:
        - Optional[List[dict]] - A list of dictionaries representing the schema of the table.
                                 Each dictionary contains details about a column
        - HTTP Status Code (int)
    """
    def get_table_schema(self, table_name: str) -> Tuple[Optional[List[dict]], int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return None, status[1]

            self.cursor().execute(f"PRAGMA table_info({table_name})")
            schema = self.cursor().fetchall()
            if not schema:
                self.logger.warning(f"Table {table_name} schema not found.")
                return None, 404

            self.logger.info(self.MESSAGES["TABLE_SCHEMA_RETRIEVED"].format(table_name=table_name))
            return schema, 200

        except Exception as e:
            self.logger.error(f"Unexpected error occurred while retrieving table schema: {str(e)}")
            return None, 500

    """
    Creates table in SQLite Database
    Parameters:
        table_name (str) - The name of the table to create
        force_create (bool) - Whether to force creation if table already exists
    Returns:
        - Message (str)
        - HTTP Status Code (int)
    """
    def create_table(self, table_name: str, columns: List[str], force: bool = False) -> Tuple[str, int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=False, force=force)
            if status is not None:
                return status

            if len(columns) == 0:
                message = "No columns provided for table creation."
                self.logger.error(message)
                return message, 400

            columns = ", ".join(columns)

            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            self.cursor().execute(query)

            self.db().commit()
            message = self.MESSAGES["TABLE_CREATED"].format(table_name=table_name)
            self.logger.info(message)

            return message, 201

        except Exception as e:
            message = f"Failed to create table {table_name}: {str(e)}"
            self.logger.error(message)
            return message, 500

    """
    Delete table from SQLite Database
    Parameters:
        table_name (str) - The name of the table to delete
    Returns:
        - Message (str)
        - HTTP Status Code (int)
    """

    def drop_table(self, table_name: str) -> Tuple[str, int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return status

            self.cursor().execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cursor().execute(f"VACUUM")
            self.db().commit()

            message = self.MESSAGES["TABLE_DELETED"].format(table_name=table_name)
            self.logger.info(message)

            return message, 200

        except Exception as e:
            message = f"{self.MESSAGES["TABLE_DELETION_FAIL"].format(table_name=table_name)}: {str(e)}"
            self.logger.error(message)
            return message, 500