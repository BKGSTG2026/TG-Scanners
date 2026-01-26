from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, Text
from tg_scanners.config.settings import DB_MESSAGE_TABLE
Base = declarative_base()

class Message(Base):
    # __tablename__ = "messages"
    __tablename__ = DB_MESSAGE_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True)

    raw = Column(String(4096), nullable=False)
    length = Column(Integer, nullable=False)
    prefix = Column(Text, nullable=False)
    tag_status = Column(Text, nullable=False)
    epc = Column(Text, nullable=False)
    dat = Column(Text, nullable=False)


    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
