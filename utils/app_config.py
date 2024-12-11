from types import SimpleNamespace

import yaml
from dotenv import dotenv_values

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_env()
            cls._instance._load_endpoints()
        return cls._instance

    def _load_env(self):
        """Load environment variables from the .env file."""
        config = dotenv_values(".env")
        self.host = config.get('HOST')
        self.server_port = config.get('FLASK_PORT')
        self.server_url = f"https://{self.host}:{self.server_port}"
        self.db_path = config.get('DB_PATH')

    def _load_endpoints(self):
        """Load endpoints from the YAML file."""
        with open('res/endpoints.yml', 'r') as file:
            endpoints = yaml.safe_load(file)
        self.database_endpoints = self.dict_to_namespace(endpoints.get('database', {}))

    def dict_to_namespace(self, d):
        return SimpleNamespace(**{k: self.dict_to_namespace(v) if isinstance(v, dict) else v for k, v in d.items()})
