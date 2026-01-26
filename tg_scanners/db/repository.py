from sqlalchemy.orm import sessionmaker
from tg_scanners.db.engine import build_engine
from tg_scanners.db.schema import ensure_schema
from tg_scanners.db.models import Message
from tg_scanners.config.settings import (
    DB_DIALECT,
    DB_DRIVER,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

class MessageRepository:
    def __init__(self):
        self.engine = build_engine(
            dialect=DB_DIALECT,
            driver=DB_DRIVER,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            username=DB_USER,
            password=DB_PASSWORD,
        )

        # Explicit schema bootstrap
        ensure_schema(self.engine)

        self.Session = sessionmaker(bind=self.engine)

    def save(self, parsed_data: dict) -> None:
        session = self.Session()
        try:
            print(f"Saving to DB: {parsed_data}")  # add this line
            session.add(Message(**parsed_data))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
