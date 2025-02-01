import os
import sqlite3
from typing import Tuple
from notelab.db.utils import to_snake_case, verify_name

class ConnectionHandler:

    def __init__(self, logger, db_name, messages):
        self.connected = None
        self.db = None
        self.db_path = None
        self.cursor = None
        self.logger = logger
        self.db_name = db_name
        self.MESSAGES = messages

    def __del__(self):
        self.disconnect()
        self.logger.info(self.MESSAGES["SQLITE_DISCONNECTED"])

    def __enter__(self):
        self.logger.info(self.MESSAGES["SQLITE_INITIALIZED"])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        self.logger.info(self.MESSAGES["SQLITE_DISCONNECTED"])

    """
    Connect to SQLite Database
    Parameters:
        db_path (str) - The path to the database file
        force_connect (bool) - Whether to force a connection if already connected
    Returns:
        Response message (str)
        HTTP Status Code (int)
    """
    def connect(self, db_path: str, force_connect: bool = False) -> Tuple[str, int]:
        self.logger.info(self.MESSAGES["INITIALIZING_CONNECTION"].format(db_name=db_path))
        db_name = os.path.basename(db_path).split('.')[0]

        try:
            db_name = to_snake_case(db_name)
            if not verify_name(db_name):
                message = self.MESSAGES["INVALID_DB_NAME"].format(db_name=db_name)
                self.logger.error(message)
                return message, 400

            db_path = db_path.strip()
            if not os.path.exists(db_path):
                message = self.MESSAGES["DB_PATH_NOT_FOUND"].format(db_path=db_path)
                self.logger.error(message)
                return message, 404

            if self.connected:
                message = self.MESSAGES["ALREADY_CONNECTED"].format(db_name=self.db_name)
                self.logger.warning(message)
                if force_connect:
                    self.logger.info(f"Force connecting to database {db_name}...")
                    self.disconnect()
                else:
                    return message, 409

            self.db_path = db_path
            self.db_name = db_name
            self.db = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.db.cursor()
            self.connected = True

            message = self.MESSAGES["CONNECT_SUCCESS"].format(db_name=self.db_name)
            self.logger.info(message)
            return message, 200

        except Exception as e:
            self.db = None
            self.db_path = None
            self.db_name = None
            self.cursor = None
            self.connected = False
            message = f"{self.MESSAGES['CONNECT_FAIL'].format(db_name=db_name)}: {str(e)}"
            self.logger.error(message)
            return message, 500

    """
    Disconnect from SQLite Database
    Parameters:
        force_disconnect (bool) - Whether to force a disconnect if not connected
    Returns:
        Response message (str)
        HTTP Status Code (int)
    """

    def disconnect(self, force_disconnect: bool = False) -> Tuple[str, int]:
        self.logger.info(self.MESSAGES["TERMINATING_CONNECTION"].format(db_name=self.db_name))
        db_name = self.db_name

        try:
            if not self.connected:
                message = self.MESSAGES["NOT_CONNECTED"]
                self.logger.info(message)
                if not force_disconnect:
                    self.logger.warning(self.MESSAGES["ALREADY_DISCONNECTED"])
                    return message, 409

            self.cursor.close()
            self.db.close()
            self.cursor = None
            self.db = None
            self.db_path = None
            self.db_name = None
            self.connected = False

            message = self.MESSAGES["DISCONNECT_SUCCESS"].format(db_name=db_name)
            self.logger.info(message)
            return message, 200

        except Exception as e:
            message = f"{self.MESSAGES['DISCONNECT_FAIL'].format(db_name=db_name)}: {str(e)}"
            self.logger.error(message)
            return message, 500