import abc
from sqlalchemy import func, text, desc, and_
from sqlalchemy.exc import CompileError, InvalidRequestError

from src.people.domain_models.models import Person
from src.people.repository.exceptions import RepositoryException


class AbstractRepository(abc.ABC):
    """ Template class for repositories """

    @abc.abstractmethod
    def add(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, model, model_id: str):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """ Repository based on SqlAlchemy orm """

    def __init__(self, session):
        self.session = session

    def add(self, model):
        """
        Add object to the database
        :param model: Model to be added
        :return:
        """

        self.session.add(model)

    def get(self, model, model_id: str):
        """
        Get single object by id
        :param model: Type of object to be retrieved
        :param model_id: Id of object to be retrieved
        :return:
        """

        return self.session.query(model).filter_by(id=model_id).one()

    def group_by_and_count(self, model, column, limit: int = None,
                           descending: bool = True):
        """
        Perform common group by and count database operation
        :param model: Model type of objects to be used
        :param column: Column to perform group by operation
        :param limit: Limit results - optional
        :param descending: Filtering the results, descending is default
        :return:
        """

        try:
            q = self.session.query(model, func.count(column)).group_by(
                column)
            if descending:
                q = q.order_by(desc(text('count_1')))
            if limit:
                q = q.limit(limit)

            return q.all()
        except CompileError:
            raise RepositoryException(f'Invalid column to group by: {column}')

    def filter_person_by_date_of_birth(self, date_1, date_2):
        """
        Specific filter to match person date of birth between two given dates
        :param date_1: Earlier date to match
        :param date_2: Later date to match
        :return:
        """
        query = self.session.query(Person).filter(and_(
            Person.date_of_birth >= date_1,
            Person.date_of_birth <= date_2))

        return query.all()

    def filter_model_by(self, model, **filters):
        """
        Perform filter by operation
        :param model: Type of model to be retrieved
        :param filters: Filters to use
        :return:
        """

        try:
            return self.session.query(model).filter_by(**filters).all()
        except InvalidRequestError:
            raise RepositoryException(f"Invalid columns given: {filters}")
