#!/usr/bin/env python3
"""
Simple Python ingestion service for Telegraf → MSSQL
"""

import sys
import pyodbc
import os
import logging
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import NVARCHAR, Column, DateTime, Integer, String, create_engine, func, text, Table, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, request, jsonify
from datetime import datetime

# -----------------------------
# Logging 
# -----------------------------

# Change the logging level to 'info' to see fewer logs, leaving as debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -----------------------------
# Flask app - http server
# -----------------------------

app = Flask(__name__)

# -----------------------------
# Load env vars from environment file
# -----------------------------

load_dotenv()

# MySQL Server connection settings
# DB_DRIVER = os.getenv("DB_DRIVER")
DB_HOST          = os.getenv("DB_HOST")
DB_PORT          = int(os.getenv("DB_PORT"))
DB_NAME          = os.getenv("DB_NAME")
DB_USER          = os.getenv("DB_USER")
DB_PASSWORD      = os.getenv("DB_PASSWORD")
DB_MESSAGE_TABLE = os.getenv("DB_MESSAGE_TABLE")
BATCH_SIZE       = int(os.getenv("BATCH_SIZE", "100"))

password_enc = urllib.parse.quote_plus(DB_PASSWORD)
# driver_enc = urllib.parse.quote_plus(DB_DRIVER)

# -----------------------------
# Database connection
# -----------------------------

# Build connection string - TODO: urlencode all values
CONNECTION_STRING = (
    f"mssql+pymssql://{DB_USER}:{password_enc}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
POLL_INTERVAL = 5

# Initialize the connection from env values
engine = create_engine(CONNECTION_STRING)

# Collect metadata for sqlalchemy
metadata = MetaData()
metadata.reflect(bind=engine)

# Create table if it doesn't already exist
if DB_MESSAGE_TABLE not in metadata.tables:
    logger.info(f"Table '{DB_MESSAGE_TABLE}' not found in database '{DB_NAME}' - creating it")
    
    table = Table(
        DB_MESSAGE_TABLE,
        metadata,
        # "Our" Columns
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("scan_time", DateTime, server_default=func.sysdatetime()),
        Column("scanner_name", String(50)),
        Column("scanner_payload", NVARCHAR(None)),

        # "Thier" Exitisting Columns
        Column("RFID_Historian_ID",  Integer),
        Column("RFIDTag_ID", NVARCHAR(50)),
        Column("Status_Date_Time", DateTime, server_default=func.sysdatetime()),
        Column("GateNumber",NVARCHAR(16)),
        Column("TrainID",NVARCHAR(10)),
        Column("TrainName",NVARCHAR(16)),
    )
else:
    table = Table(DB_MESSAGE_TABLE, metadata, autoload_with=engine)

metadata.create_all(engine)

# Refresh metadata
metadata.clear()
metadata.reflect(bind=engine)

# -----------------------------
# Ingest endpoint (runs at http://127.0.0.1:5000/ingest)
# This is where telegraf sends its data to
# -----------------------------
 
# Define route - only accept POST requests
@app.route("/ingest", methods=["POST"])
def ingest():
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        records = extract_value_records(data)
        logger.info(f"Received {len(data)} records")
        logger.debug(f"Record: {data}")
        
        insert_records(records)
        return "", 204

    except Exception as e:
        logger.exception("Error processing ingest request")
        return jsonify({"error": str(e)}), 500

# Testing endpoint that can be used to check the status of the application
# ex) curl localhost:5000/health if testing from local machine
@app.route("/health")
def health():
    logger.info("Health status ping")
    return "OK", 200

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
    logger.debug(f"Parsing payload of {metrics}")
    for metric in metrics:
        fields = metric.get("fields", {})
        logger.debug(f"fields: {fields}")

        # Get the timestamp from the telegraf scan which uses epoch time
        ts = metric.get("timestamp")
        logger.debug(f"timestamp: {ts}")

        # Get the scanner_name as defined in the telegraf config
        scanner_name = metric.get("name", {})
        logger.debug(f"scanner_name: {scanner_name}")

        # Insert the raw scanner payload (data) into the database
        # should probably be parsed into separate valuses, but works for now
        scanner_payload = fields.get("value", "UNKNOWN")
        logger.debug(f"scanner_payload: {scanner_payload}")

        # Define the fields that are written to the database
        record = {
            "scanner_payload": scanner_payload,
            "scan_time": datetime.fromtimestamp(ts),
            "scanner_name": scanner_name
        }
        records.append(record)
    return records

# -----------------------------
# Database logic
# -----------------------------

def insert_records(records):
    """
    Insert data into the MSSQL table using SQLAlchemy.
    """
    if not records:
        logger.debug("No records found")
        return

    try:
        with engine.begin() as conn:
            batch = []
            for record in records:
                batch.append(record)
                if len(batch) >= BATCH_SIZE:
                    conn.execute(insert(table), batch)
                    logger.debug(f"Inserted {len(batch)} record into database")
                    batch = []

            # Insert any remaining
            if batch:
                conn.execute(insert(table), batch)
                logger.debug(f"Inserted {len(batch)} record into database")

        logger.info(f"Inserted {len(records)} records into {DB_MESSAGE_TABLE}")

    except SQLAlchemyError as e:
        logger.exception("Database insertion error")
        raise

# -----------------------------
# Run server
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
