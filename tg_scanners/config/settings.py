"""
Parse .env file and load values into ENV vars that python can use
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Scanner connection addresses
TCP_HOST_SCANNER1 = os.getenv("TCP_HOST_SCANNER1")
TCP_SCANNER_PORT = int(os.getenv("LISTEN_PORT", 7000))

# MySQL Server connection settings
DB_DIALECT = os.getenv("DB_DIALECT")
DB_DRIVER = os.getenv("DB_DRIVER")
DRIVER_PATH = os.getenv("DRIVER_PATH")
DB_MESSAGE_TABLE = os.getenv("DB_MESSAGE_TABLE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

