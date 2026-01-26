from sqlalchemy.engine import Engine
from tg_scanners.db.models import Base

def ensure_schema(engine: Engine) -> None:
    """
    Create all tables if they do not already exist.

    Safe to call multiple times.
    """
    Base.metadata.create_all(engine)
