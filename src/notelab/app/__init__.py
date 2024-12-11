import os
import sys

# Add the parent directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from . import app
from notelab import db
import utils

__all__ = ['app', 'db', 'utils']