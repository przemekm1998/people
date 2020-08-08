from datetime import date

import pytest

from src.people.domain_models.models import Person
from src.people.repository.exceptions import RepositoryException
from src.people.repository.repository import SqlAlchemyRepository


def insert_person(session, gender, title, first_name, second_name, date_of_birth):
    session.execute(
        'INSERT INTO "person" (gender, title, first_name, second_name, date_of_birth) '
        'VALUES '
        '(:gender, :title, :first_name, :second_name, :date_of_birth)',
        dict(gender=gender, title=title, first_name=first_name,
             second_name=second_name, date_of_birth=date_of_birth)
    )
    [[person_id]] = session.execute(
        'SELECT id FROM person WHERE gender=:gender AND title=:title AND '
        'first_name=:first_name AND second_name=:second_name AND '
        'date_of_birth=:date_of_birth',
        dict(gender=gender, title=title, first_name=first_name,
             second_name=second_name, date_of_birth=date_of_birth)
    )

    return person_id


def populated_db_fixture(session):
    insert_person(session, 'male', 'mr', 'john', 'doe', '1997-01-01')
    insert_person(session, 'male', 'mr', 'mike', 'doe', '1998-01-01')
    insert_person(session, 'female', 'ms', 'jane', 'smith', '1999-01-01')


def test_repository_can_save_user(session, user_fixture):
    user = user_fixture

    repo = SqlAlchemyRepository(session)
    repo.add(user)
    session.commit()

    rows = list(session.execute(
        'SELECT * FROM user'
    ))
    assert rows == [(1, 1, 1, 1, 1, 1)]


def test_repository_can_retrieve_model(session):
    person_id = insert_person(session, 'male', 'mr', 'john', 'doe', '1997-01-01')

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get(Person, person_id)

    expected_person = Person('male', 'mr', 'john', 'doe',
                             date.fromisoformat('1997-01-01'))

    assert retrieved.gender == expected_person.gender
    assert retrieved.title == expected_person.title
    assert retrieved.first_name == expected_person.first_name
    assert retrieved.second_name == expected_person.second_name
    assert retrieved.date_of_birth == expected_person.date_of_birth


def test_repository_group_by(session):
    populated_db_fixture(session)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.group_by_and_count(Person, 'gender', limit=1)

    assert retrieved[0][0].gender == 'male'
    assert retrieved[0][1] == 2


def test_repository_group_by_not_existing_column(session):
    populated_db_fixture(session)

    repo = SqlAlchemyRepository(session)
    with pytest.raises(RepositoryException):
        retrieved = repo.group_by_and_count(Person, 'idontexist', limit=1)


def test_repository_filter_by_between(session):
    populated_db_fixture(session)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.filter_person_by_date_of_birth(date.fromisoformat('1998-01-01'),
                                                    date.fromisoformat('1999-01-01'))

    assert len(retrieved) == 2
    assert retrieved[0].date_of_birth == date.fromisoformat('1998-01-01')
    assert retrieved[1].date_of_birth == date.fromisoformat('1999-01-01')


def test_filter_by(session):
    populated_db_fixture(session)

    repo = SqlAlchemyRepository(session)
    filters = {'gender': 'male', 'date_of_birth': date.fromisoformat('1998-01-01')}
    retrieved = repo.filter_model_by(Person, **filters)

    assert retrieved[0].gender == 'male'
    assert retrieved[0].date_of_birth == date.fromisoformat('1998-01-01')


def test_filter_by_not_existing_columns(session):
    populated_db_fixture(session)

    repo = SqlAlchemyRepository(session)
    filters = {'idontexist': 'male', 'andmetoo': date.fromisoformat('1998-01-01')}

    with pytest.raises(RepositoryException):
        retrieved = repo.filter_model_by(Person, **filters)
