import os
import pyodbc
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

# List all ODBC drivers
print("ODBC Drivers installed on this system:")
for driver in pyodbc.drivers():
    print(driver)

# Test creating a DSN-less connection string (won't actually connect)
driver_name = "ODBC Driver 18 for SQL Server"
conn_str = f"DRIVER={{{driver_name}}};SERVER=localhost;UID=sa;PWD={{{DB_PASSWORD}}};TrustServerCertificate=yes"

try:
    conn = pyodbc.connect(conn_str, timeout=1)
except Exception as e:
    print("Driver callable — connection test failed as expected:")
    print(e)