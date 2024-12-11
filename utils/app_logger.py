import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a rotating file handler for each class
    handler = RotatingFileHandler(f'logs/{name}.log', maxBytes=10000000, backupCount=3)
    handler.setLevel(logging.DEBUG)

    # Set formatter for logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)
    return logger
