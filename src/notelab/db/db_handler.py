"""
This class is responsible for handling SQL database operations
"""

from functools import wraps
from typing import Tuple, Any, Callable
import json
import os

from .connection_handler import ConnectionHandler
from .row_handler import RowHandler
from .table_handler import TableHandler
from ..utils.app_logger import setup_logger


def connection_required(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._connect(self.db_name)
        try:
            result = func(self, *args, **kwargs)
        finally:
            self._disconnect()
        return result
    return wrapper

class DBHandler:

    _instance = None

    def __new__(cls, db_name: str):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
            cls._instance._initialize(db_name)
        return cls._instance

    def _initialize(self, db_name: str):
        self.logger = setup_logger()
        self.messages = json.load(open(os.path.join(os.path.dirname(__file__), 'messages.json')))
        self.connection_handler = ConnectionHandler(self.logger, db_name, self.messages)
        self.table_handler = TableHandler(self.logger, db_name, self.messages, self.connection_handler)
        self.row_handler = RowHandler(self.logger, db_name, self.messages, self.connection_handler, self.table_handler)

    def validate_table_status(self, table_name: str, exist_condition: bool = False) -> Tuple[str, int]:
        return self.table_handler.validate_table_status(table_name, exist_condition)

    def _connect(self, db_path) -> Tuple[str, int]:
        return self.connection_handler.connect(db_path)

    def _disconnect(self) -> Tuple[str, int]:
        return self.connection_handler.disconnect()

    @connection_required
    def get_tables(self) -> Tuple[Any, int]:
        return self.table_handler.get_tables()

    @connection_required
    def get_table(self, table_name: str) -> Tuple[Any, int]:
        return self.table_handler.get_table(table_name)

    @connection_required
    def create_table(self, table_name, columns) -> Tuple[Any, int]:
        return self.table_handler.create_table(table_name, columns)

    @connection_required
    def get_table_schema(self, table_name) -> Tuple[Any, int]:
        return self.table_handler.get_table_schema(table_name)

    @connection_required
    def drop_table(self, table_name) -> Tuple[Any, int]:
        return self.table_handler.drop_table(table_name)

    @connection_required
    def get_row(self, table_name, row_id):
        return self.row_handler.get_row(table_name, row_id)

    @connection_required
    def get_rows(self, table_name, conditions):
        return self.row_handler.get_rows(table_name, conditions)

    @connection_required
    def insert_rows(self, table_name, data):
        return self.row_handler.insert_rows(table_name, data)

    @connection_required
    def update_rows(self, table_name, data):
        return self.row_handler.update_rows(table_name, data)