from utils.app_logger import setup_logger
from .connection_handler import ConnectionHandler

class DBHandler:
    def __init__(self, db_name):
        self.logger = setup_logger('app')
        self.connection_handler = ConnectionHandler(db_name)

    def close(self):
        self.connection_handler.disconnect()

    def connect(self, db_path):
        self.connection_handler.connect(db_path)

    def get_tables(self):
        pass

    def get_table(self, table_name):
        pass

    def create_table(self, table_name, columns):
        pass

    def get_table_schema(self, table_name):
        pass

    def drop_table(self, table_name):
        pass

    def get_row(self, table_name, row_id):
        pass

    def get_rows(self, table_name, conditions):
        pass

    def insert_rows(self, table_name, data):
        pass

    def update_rows(self, table_name, data):
        pass