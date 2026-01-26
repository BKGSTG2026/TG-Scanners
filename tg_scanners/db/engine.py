import urllib.parse
import pyodbc
from sqlalchemy import create_engine

def build_conn_str(
    dialect: str,
    driver_path: str,
    driver: str,
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
): 
    print(locals())
    return (
        f"DRIVER={{{driver_path}}};"
        f"SERVER={{{host}}};"
        f"DATABASE={{{database}}};"
        f"UID={{{username}}};"
        f"PWD={{{password}}};"
        f"PORT={{{port}}};"
        "MULTI_HOST=1"
    )

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
        return create_engine(
            f"""mysql+pyodbc:///?odbc_connect={
                build_conn_str(
                    dialect,
                    driver_path,
                    driver,
                    host,
                    port,
                    database,
                    username,
                    password
                )
            }"""
        )

    raise ValueError(f"Unsupported DB dialect: {dialect}")

