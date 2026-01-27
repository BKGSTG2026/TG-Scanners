"""
Initialize the database connection - only supports mysql dbs
"""

import urllib.parse
import pyodbc
from sqlalchemy import create_engine

def build_engine(
    dialect: str,
    driver_path: str,
    driver: str,
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
):
    if dialect == "mysql":
        # Create the mysql connection string from the .env file values
        return create_engine(
            f"""mysql+pyodbc:///?odbc_connect={
                f"DRIVER={{{driver_path}}};"
                f"SERVER={{{host}}};"
                f"DATABASE={{{database}}};"
                f"UID={{{username}}};"
                f"PWD={{{password}}};"
                f"PORT={{{port}}};"
                "MULTI_HOST=1"
            }"""
        )

    raise ValueError(f"Unsupported DB dialect: {dialect}")

