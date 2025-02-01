import threading
from types import SimpleNamespace
import yaml
from dotenv import dotenv_values
from notelab.utils.app_logger import setup_logger

class AppConfig:
    _instance = None
    _lock = threading.Lock()

    logger = setup_logger('Config')

    def __new__(cls):
        with cls._lock:  # Only one thread can enter this block at a time
            if cls._instance is None:
                cls._instance = super(AppConfig, cls).__new__(cls)
                cls._instance._load_env()
                cls._instance._load_endpoints()
        return cls._instance

    def _load_env(self):
        """Load environment variables from the .env file."""
        try:
            _config = dotenv_values(".env")
            self.host = _config.get('HOST')
            self.server_port = _config.get('FLASK_PORT')
            self.server_url = f"https://{self.host}:{self.server_port}"
            self.db_path = _config.get('DB_PATH')
            self.logger.info("Environment variables loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load environment variables: {e}")
            raise

    def _load_endpoints(self):
        """Load endpoints from the YAML file."""
        try:
            with open('res/endpoints.yml', 'r') as file:
                endpoints = yaml.safe_load(file)
            self.database_endpoints = self.dict_to_namespace(endpoints.get('database', {}))
            self.logger.info("Endpoints loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load endpoints: {e}")
            raise

    def dict_to_namespace(self, d):
        return SimpleNamespace(**{k: self.dict_to_namespace(v) if isinstance(v, dict) else v for k, v in d.items()})
