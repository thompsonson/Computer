"""
holds the logic for accessing the database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


def create_engine_and_session(base_sqlalchemy_class, echo=False):
    """creates the sqlite db engine and returns a session to it"""

    engine = create_engine(f"{settings.DATABASE}", echo=echo, future=True)
    base_sqlalchemy_class.metadata.create_all(engine)

    engine_session = sessionmaker(bind=engine)

    return engine_session()
