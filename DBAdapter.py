"""
holds the logic for accessing the database
"""
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.model_notes import notes_base


import settings

engine = create_engine(
    f"{settings.SQLA_CONNECTION_STRING}",
    echo=settings.SQLA_ECHO,
    future=settings.SQLA_FUTURE,
)
# create the tables if they don't exist
notes_base.metadata.create_all(engine)


class DBAdapter:
    """A class that holds the logic for accessing the database"""

    @contextmanager
    def session(self, local_engine=engine) -> Generator[sessionmaker, None, None]:
        """Creates a session, commits at the end, rolls back on exception, removes.

        Yields:
            a session object. The session will .commit() when a `with DBAdapter.session()`
            statement terminates normally, or .rollback() on an exception.
        """
        try:
            session = sessionmaker(bind=local_engine)
            # transaction has already begun here, so no explicit .begin().
            yield session
        except:
            session.rollback()  # type: ignore
            raise
        else:
            session.commit()  # type: ignore
        finally:
            # Note: close() unbinds model objects, but keeps the DB connection.
            session.close()  # type: ignore
            # TODO: does anything else need to be done to cleanup the session?
