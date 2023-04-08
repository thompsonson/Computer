"""
holds the logic for accessing the database
"""
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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

    def __init__(self):
        self._session = None

    @contextmanager
    def managed_session(self, local_engine=engine) -> Generator[Session, None, None]:
        """Creates a session, commits at the end, rolls back on exception, removes.

        Yields:
            a session object. The session will .commit() when a `with DBAdapter.managed_session()`
            statement terminates normally, or .rollback() on an exception.
        """
        try:
            self._session = Session(bind=local_engine)
            # self._session = sessionmaker()
            self._session.begin()
            yield self._session
        except:
            self._session.rollback()  # type: ignore
            raise
        else:
            self._session.commit()  # type: ignore
        finally:
            # Note: close() unbinds model objects, but keeps the DB connection.
            self._session.close()  # type: ignore
            # TODO: does anything else need to be done to cleanup the session?
