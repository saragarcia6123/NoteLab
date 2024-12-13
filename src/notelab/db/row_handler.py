import logging
import sqlite3
from typing import List, Optional, Tuple
from notelab.db.connection_handler import ConnectionHandler
from notelab.db.table_handler import TableHandler


class RowHandler:

    def __init__(self, logger: logging.Logger, db_name: str, messages: dict, connection_handler: ConnectionHandler, table_handler: TableHandler):
        self.logger = logger
        self.MESSAGES = messages
        self.db_name = db_name
        self.connection_handler = connection_handler
        self.table_handler = table_handler

    def connected(self) -> bool:
        return self.connection_handler.connected

    def cursor(self) -> sqlite3.Cursor:
        return self.connection_handler.cursor

    def db(self) -> sqlite3.Connection:
        return self.connection_handler.db

    def validate_table_status(self, table_name: str, exist_condition: bool = False) -> Optional[Tuple[str, int]]:
        return self.table_handler.validate_table_status(table_name, exist_condition)
    
    def get_primary_key_column(self, table_name: str) -> Optional[str]:
        self.cursor().execute(f"PRAGMA table_info({table_name})")
        primary_key_column = None
        for column_info in self.cursor().fetchall():
            if column_info[5] == 1:  # pk flag is column 5 in PRAGMA table_info
                primary_key_column = column_info[1]  # Index 1 is column name
                break
        return primary_key_column

    """
    Retrieves a row based on primary key from table in SQLite Database
    Parameters:
        - table_name (str) - The name of the table to retrieve row from
        - row_id (str) - The value of the primary key of the row to retrieve
    Returns:
        - A dictionary representing the row of the table if found, None otherwise
        - HTTP Status Code (int)
    """
    def get_row(self, table_name: str, primary_key_value: str) -> Tuple[Optional[dict], int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return None, status[1]

            primary_key_column = self.get_primary_key_column(table_name)

            query = f"SELECT * FROM {table_name} WHERE {primary_key_column} = ?"
            self.cursor().execute(query, (primary_key_value,))
            row = self.cursor().fetchone()

            if row is None:
                self.logger.info(self.MESSAGES["ROW_NOT_FOUND"].format(table_name=table_name, row_id=primary_key_value))
                return None, 404

            column_names = [description[0] for description in self.cursor().description]
            row_data = dict(zip(column_names, row))

            self.logger.info(self.MESSAGES["ROW_RETRIEVAL_SUCCESS"].format(table_name=table_name, row_id=primary_key_value))
            return row_data, 200

        except Exception as e:
            message = f"{self.MESSAGES['ROWS_RETRIEVAL_FAILED'].format(table_name=table_name)}: {str(e)}"
            self.logger.error(message)
            return None, 500

    """
    Retrieves rows from table in SQLite Database based on conditions
    Parameters:
        - table_name (str) - The name of the table to retrieve rows from
        - conditions (List[str]) - A list of conditions to filter the rows by
    Returns:
        - A list of dictionaries representing the rows of the table if found, None otherwise
        - HTTP Status Code (int)
    """
    def get_rows(self, table_name: str, conditions: List[str]) -> Tuple[Optional[List[dict]], int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return None, status[1]

            condition_str = " AND ".join(conditions) if conditions else "1=1"  # Select all if no conditions
            query = f"SELECT * FROM {table_name} WHERE {condition_str}"
            self.cursor().execute(query)
            columns = [column[0] for column in self.cursor().description]
            rows = [dict(zip(columns, row)) for row in self.cursor().fetchall()]

            message = self.MESSAGES["ROWS_FOUND"].format(table_name=table_name)
            self.logger.info(message)

            return rows, 200

        except Exception as e:
            message = f"{self.MESSAGES['ROWS_RETRIEVAL_FAILED'].format(table_name=table_name)}: {str(e)}"
            self.logger.error(message)
            return None, 500

    """
    Insert row into table in SQLite Database
    Parameters:
        table_name (str) - The name of the table to insert row into
        row (List[str]) - The row data to insert
    Returns:
        Response message (str)
        HTTP Status Code (int)
    """
    def insert_row(self, table_name: str, row: List[str]) -> Tuple[str, int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return status

            placeholders = ", ".join(["?" for _ in row])
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            self.cursor().execute(insert_query, row)
            self.db().commit()

            message = self.MESSAGES["ROW_INSERTED"].format(table_name=table_name)
            self.logger.info(message)
            return message, 201

        except Exception as e:
            message = self.MESSAGES["ROWS_INSERTION_FAIL"].format(table_name=table_name) + f" {str(e)}"
            self.logger.error(message)
            return message, 500

    """
    Insert multiple rows into table in SQLite Database
    Parameters:
        - table_name (str) - The name of the table to insert rows into
        - rows (List[List[str]]) - A list of row data to insert
    Returns:
        Response message (str)
        HTTP Status Code (int)
    """
    def insert_rows(self, table_name: str, rows: List[List[str]]) -> Tuple[str, int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return status

            self.cursor().execute(f"PRAGMA table_info({table_name})")
            columns_info = self.cursor().fetchall()
            column_names = [info[1] for info in columns_info]

            placeholders = ', '.join(['?' for _ in column_names])
            insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"

            self.cursor().executemany(insert_query, rows)
            self.db().commit()

            message = self.MESSAGES["ROWS_INSERTION_SUCCESS"].format(table_name=table_name)
            self.logger.info(message)

            return message, 201

        except Exception as e:
            message = self.MESSAGES["ROWS_INSERTION_FAIL"].format(table_name=table_name) + f" {str(e)}"
            self.logger.error(message)
            return message, 500

    """
    Delete rows from table in SQLite Database
    Parameters:
        - table_name (str) - The name of the table to delete rows from
    Returns:
        - True if rows deleted, False otherwise
        - HTTP Status Code (int)
    """
    def delete_rows(self, table_name: str, conditions: List[str]) -> Tuple[str, int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return status

            condition_str = " AND ".join(conditions)
            delete_query = f"DELETE FROM {table_name} WHERE {condition_str}"
            self.cursor().execute(delete_query)

            self.db().commit()

            message = self.MESSAGES["ROWS_DELETED"].format(table_name=table_name)
            self.logger.info(message)
            return message, 200

        except Exception as e:
            message = f"{self.MESSAGES['ROWS_DELETION_FAILED'].format(table_name=table_name)} {str(e)}"
            self.logger.error(message)
            return message, 500

    """
    Update multiple rows in a table in SQLite Database
    Parameters:
        - table_name (str) - The name of the table to update rows in
        - rows (List[List[str]]) - A list of tuples, each containing the unique identifier followed by the column data
    Returns:
        Response message (str)
        HTTP Status Code (int)
    """

    def update_rows(self, table_name: str, rows: List[List[str]]) -> Tuple[str, int]:
        try:
            status = self.validate_table_status(table_name=table_name, exist_condition=True)
            if status is not None:
                return status

            self.cursor().execute(f"PRAGMA table_info({table_name})")
            columns_info = self.cursor().fetchall()
            column_names = [info[1] for info in columns_info]

            if len(column_names) < 2:
                message = "Table must have at least a unique identifier and one field to update."
                self.logger.warning(message)
                return message, 400

            identifier_col = column_names[0]
            update_columns = column_names[1:]

            set_clause = ', '.join([f"{column} = ?" for column in update_columns])
            update_query_template = f"UPDATE {table_name} SET {set_clause} WHERE {identifier_col} = ?"

            with self.db:
                for row in rows:
                    if len(row) != len(column_names):
                        message = f"Row length {len(row)} does not match table column count {len(column_names)}"
                        self.logger.error(message)
                        continue

                    unique_id = row[0]
                    values = row[1:]

                    self.cursor().execute(update_query_template, values + [unique_id])

            self.db().commit()
            message = self.MESSAGES["ROWS_UPDATE_SUCCESS"].format(table_name=table_name)
            self.logger.info(message)

            return message, 200

        except Exception as e:
            message = self.MESSAGES["ROWS_UPDATE_FAIL"].format(table_name=table_name) + f" {str(e)}"
            self.logger.error(message)
            return message, 500