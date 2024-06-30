from typing import Dict, List, Any
from dotenv import dotenv_values
from wasabi import msg
import logging
import os

logging.basicConfig(
  filename='app.log',
  encoding='utf-8',
  level=logging.INFO,
  format='%(asctime)s %(levelname)s [module:(%(module)s) line:%(lineno)d]: %(message)s',
  datefmt='%d-%m-%Y %H:%M',
)

BASE_DIR = os.path.dirname(__file__)
PATH_IMG = os.path.join(BASE_DIR, 'images')

config = dotenv_values()
logger = logging.getLogger()

URL = config.get("URL")
HOST_MONGO = config.get("HOST_MONGO")
DATABASE_MONGO = config.get("DATABASE_MONGO")