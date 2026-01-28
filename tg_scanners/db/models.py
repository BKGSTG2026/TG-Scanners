"""
Define the schema of the "messages" table (exact name defined in .env file)
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, Text
from tg_scanners.config.settings import DB_MESSAGE_TABLE
Base = declarative_base()

class Message(Base):
    __tablename__ = DB_MESSAGE_TABLE

    # Define basic ID that auto-increments
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Define columns
    raw = Column(String(4096), nullable=False)
    length = Column(Integer, nullable=False)
    prefix = Column(Text, nullable=False)
    tag_status = Column(Text, nullable=False)
    epc = Column(Text, nullable=False)
    dat = Column(Text, nullable=False)

    # Add timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
