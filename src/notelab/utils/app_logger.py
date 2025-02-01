import inspect
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def get_class_name() -> str:
    frame = inspect.currentframe()
    while frame:
        if 'self' in frame.f_locals:
            return frame.f_locals['self'].__class__.__name__
        frame = frame.f_back
    return 'root'

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        name = get_class_name()

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Determine the log file name based on the environment
    log_file = 'app_test' if os.getenv('TEST_ENV') == 'true' else 'app'

    # Create a rotating file handler for each class
    handler = RotatingFileHandler(f'logs/{log_file}.log', maxBytes=10000000, backupCount=3)
    handler.setLevel(logging.DEBUG)

    # Set formatter for logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
