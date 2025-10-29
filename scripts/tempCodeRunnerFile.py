import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db