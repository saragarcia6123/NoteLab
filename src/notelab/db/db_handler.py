"""
This class is responsible for handling SQL database operations
"""

from typing import Tuple, Any
from notelab.db.row_handler import RowHandler
from notelab.db.table_handler import TableHandler
from utils.app_logger import setup_logger
from .connection_handler import ConnectionHandler
import json
import os

class DBHandler:
    def __init__(self, db_name: str):
        self.logger = setup_logger()
        self.messages = json.load(open(os.path.join(os.path.dirname(__file__), 'messages.json')))
        self.connection_handler = ConnectionHandler(self.logger, db_name, self.messages)
        self.table_handler = TableHandler(self.logger, db_name, self.messages, self.connection_handler)
        self.row_handler = RowHandler(self.logger, db_name, self.messages, self.connection_handler, self.table_handler)

    def validate_table_status(self, table_name: str, exist_condition: bool = False) -> Tuple[str, int]:
        return self.table_handler.validate_table_status(table_name, exist_condition)

    def connect(self, db_path) -> Tuple[str, int]:
        return self.connection_handler.connect(db_path)

    def disconnect(self) -> Tuple[str, int]:
        return self.connection_handler.disconnect()

    def get_tables(self) -> Tuple[Any, int]:
        return self.table_handler.get_tables()

    def get_table(self, table_name: str) -> Tuple[Any, int]:
        return self.table_handler.get_table(table_name)

    def create_table(self, table_name, columns) -> Tuple[Any, int]:
        return self.table_handler.create_table(table_name, columns)

    def get_table_schema(self, table_name) -> Tuple[Any, int]:
        return self.table_handler.get_table_schema(table_name)

    def drop_table(self, table_name) -> Tuple[Any, int]:
        return self.table_handler.drop_table(table_name)

    def get_row(self, table_name, row_id):
        return self.row_handler.get_row(table_name, row_id)

    def get_rows(self, table_name, conditions):
        return self.row_handler.get_rows(table_name, conditions)

    def insert_rows(self, table_name, data):
        return self.row_handler.insert_rows(table_name, data)

    def update_rows(self, table_name, data):
        return self.row_handler.update_rows(table_name, data)