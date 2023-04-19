"""
holds the logic for accessing the database
"""
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.sql.notes import notes_base
from models.sql.ethicalai import Base as ethicalai_base
from models.sql.html import Base as html_base

import utils.settings as settings

engine = create_engine(
    f"{settings.SQLA_CONNECTION_STRING}",
    echo=settings.SQLA_ECHO,
    future=settings.SQLA_FUTURE,
)
# create the tables if they don't exist
notes_base.metadata.create_all(engine)
ethicalai_base.metadata.create_all(engine)
html_base.metadata.create_all(engine)


class DBAdapter:
    """A class that holds the logic for accessing the database"""

    def __init__(self):
        self._session = None

    def unmanaged_session(self, local_engine=engine) -> Session:
        """Creates a session, commits at the end, rolls back on exception, removes.

        Returns:
            a session object, the receiving code is responsible for calling .begin(), .commit() or .rollback()
        """
        self._session = Session(bind=local_engine)
        return self._session

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
            self._session.close()  # type: ignore
