import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.people.repository.repository import SqlAlchemyRepository


class AbstractDbConnection(abc.ABC):
    """ Database connection class pattern for other orms """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
    'sqlite:///ppl_db'
))


class SqlAlchemyDbConnection(AbstractDbConnection):
    """ Db Connection class for SqlAlchemy orm """

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.database = SqlAlchemyRepository(self.session)

        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super(SqlAlchemyDbConnection, self).__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
