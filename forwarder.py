import time
import json
import pyodbc
import shutil
import time
import json
import os
import shutil
from sqlalchemy import create_engine, text

import urllib.parse
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
DB_MESSAGE_TABLE = os.getenv("DB_MESSAGE_TABLE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SCAN_DIR = os.getenv("SCAN_DIR")

password_enc = urllib.parse.quote_plus(DB_PASSWORD)
driver_enc = urllib.parse.quote_plus(DB_DRIVER)

DB_URL = (
        f"mssql+pymssql://{DB_USER}:{password_enc}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
POLL_INTERVAL = 5

engine = create_engine(DB_URL, pool_pre_ping=True)

CREATE_TABLE_SQL = """
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='barcode_scans')
BEGIN
    CREATE TABLE barcode_scans (
        id INT IDENTITY PRIMARY KEY,
        scan_time DATETIME2 DEFAULT SYSUTCDATETIME(),
        barcode NVARCHAR(256),
        source NVARCHAR(64)
    );
END
"""

INSERT_SQL = """
INSERT INTO barcode_scans (barcode, source)
VALUES (:barcode, :source)
"""

def ensure_table():
    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLE_SQL))


def process_batch(records):
    rows = []

    for r in records:
        rows.append({
            "barcode": r.get("value"),
            "source": r.get("tags", {}).get("source", "scanner")
        })

    if not rows:
        return

    print("Throwing data in the db")
    with engine.begin() as conn:
        conn.execute(text(INSERT_SQL), rows)


def main():
    print("Starting MSSQL forwarder...")

    ensure_table()

    while True:
        try:
            files = sorted(os.listdir(SCAN_DIR))

            for fname in files:
                path = os.path.join(SCAN_DIR, fname)

                if not fname.endswith(".json"):
                    continue

                with open(path) as f:
                    records = [json.loads(l) for l in f]

                process_batch(records)
                os.remove(path)

            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(10)


if __name__ == "__main__":
    main()