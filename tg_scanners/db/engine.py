import urllib.parse
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
    if dialect == "sqlite":
        return create_engine(f"sqlite:///{database}")

    if dialect == "mysql":
        driver_enc = urllib.parse.quote_plus(driver)
        password_enc = urllib.parse.quote_plus(password)

        # connection_url = (
        #     f"mysql+pyodbc://{username}:{password_enc}"
        #     f"@{host}:{port}/{database}"
        #     f"?driver={driver_enc}"
        # )
        #using a DSN
        print("mysql+pyodbc:///?dsn=MySQL9.6")
        connection_url = "mysql+pyodbc:///?dsn=MySQL9.6"
        connection_url = "mysql+pyodbc://test:cats@127.0.0.1:3306/test1?driver=MySQL+ODBC+9.6+Unicode+Driver"

        # return create_engine(
        #     connection_url,
        #     pool_pre_ping=True,
        #     pool_recycle=3600,
        # )
        return create_engine("mysql+pyodbc:///?dsn=MySQL9.6")

    raise ValueError(f"Unsupported DB dialect: {dialect}")

