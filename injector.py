#!/usr/bin/env python3
"""
Simple Python ingestion service for Telegraf → MSSQL
"""

from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine, text
import urllib.parse
from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

load_dotenv()

# -----------------------------
# Logging
# -----------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Flask app
# -----------------------------

app = Flask(__name__)

# -----------------------------
# Database connection
# -----------------------------

# MySQL Server connection settings
DB_DRIVER = os.getenv("DB_DRIVER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_MESSAGE_TABLE = os.getenv("DB_MESSAGE_TABLE")

SCAN_DIR = os.getenv("SCAN_DIR")

password_enc = urllib.parse.quote_plus(DB_PASSWORD)
driver_enc = urllib.parse.quote_plus(DB_DRIVER)

CONNECTION_STRING = (
    f"mssql+pymssql://{DB_USER}:{password_enc}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
POLL_INTERVAL = 5
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "100"))

engine = create_engine(CONNECTION_STRING)

metadata = MetaData()
metadata.reflect(bind=engine)
if DB_MESSAGE_TABLE not in metadata.tables:
    logger.warning(f"Table '{DB_MESSAGE_TABLE}' not found in database. You must create it first.")
table = Table(DB_MESSAGE_TABLE, metadata, autoload_with=engine)


# -----------------------------
# Ingest endpoint
# -----------------------------

@app.route("/ingest", methods=["POST"])
def ingest():
    try:
        data = request.json
        print ("---------DATA", data, "--------------\n")
        
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        records = extract_value_records(data)
        logger.info(f"Received {len(data)} records")
        
        insert_records(records)
        return "", 204

    except Exception as e:
        logger.exception("Error processing ingest request")
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Transform Telegraf JSON
# -----------------------------
def extract_value_records(payload):
    """
    Converts Telegraf JSON into a list of records for DB insertion.
    Expects payload like:
    {
        "metrics": [
            {"fields": {"value": "cats"}, "timestamp": 1770430674, ...},
            ...
        ]
    }
    """
    records = []

    metrics = payload.get("metrics", [])
    for metric in metrics:
        fields = metric.get("fields", {})
        ts = metric.get("timestamp")

        record = {
            "value": fields.get("value", "UNKNOWN"),
            "time": datetime.utcfromtimestamp(ts) if ts else datetime.utcnow()
        }
        records.append(record)

    return records

# -----------------------------
# Database logic
# -----------------------------

def insert_records(records):
    """
    Insert a list of dictionaries into the MSSQL table using SQLAlchemy.
    """
    if not records:
        return

    print(records)
     # Fill missing 'time' column with UTC now
    for record in records:
        if "time" not in record or not record["time"]:
            record["time"] = datetime.utcnow()

    try:
        with engine.begin() as conn:
            batch = []
            for record in records:
                batch.append(record)
                if len(batch) >= BATCH_SIZE:
                    conn.execute(insert(table), batch)
                    batch = []

            # Insert any remaining
            if batch:
                conn.execute(insert(table), batch)

        logger.info(f"Inserted {len(records)} records into {DB_MESSAGE_TABLE}")

    except SQLAlchemyError as e:
        logger.exception("Database insertion error")
        raise

# -----------------------------
# Run server
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
