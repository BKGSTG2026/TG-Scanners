"""
Initialize the database connection - only supports mysql dbs
"""

import urllib.parse
import pyodbc
from sqlalchemy import create_engine

def build_engine(
    dialect: str,
    driver: str,
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
):
    if dialect == "mssql":
        # Create the mysql connection string from the .env file values

        # TODO: Make all variables uel-encoded
        password_enc = urllib.parse.quote_plus(password)
        driver_enc = urllib.parse.quote_plus(driver)
        
        # You can use this format instead for running on Windows using the mssql driver
        # connection_string = (
        #     f"{dialect}+pyodbc://{username}:{password_enc}@{host},{port}/{database}"
        #     f"?driver={driver_enc}"
        #     f"&Encrypt=yes"
        #     f"&TrustServerCertificate=yes"
        # )
        
        connection_string = (
        f"mssql+pymssql://{username}:{password_enc}"
        f"@{host}:{port}/{database}"
    )
        print(connection_string)
        return create_engine(
            connection_string,
            # The below can be uncommented if using the mssql driver
            # fast_executemany=True,       # improves bulk inserts
            pool_size=10,                # max concurrent connections
            max_overflow=5,              # extra connections beyond pool
            pool_pre_ping=True,          # detect stale connections
        )

    raise ValueError(f"Unsupported DB dialect: {dialect}")

