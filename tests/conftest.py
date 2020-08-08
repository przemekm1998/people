from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.people.domain_models.models import Person, ContactInfo, Timezone, Coordinates, \
    Nat, Location, PersonalId, LoginInfo, User
from src.people.repository.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture(scope='function')
def user_fixture(session):
    person = Person('male', 'mr', 'john', 'doe', date.fromisoformat('1997-01-01'))
    contact_info = ContactInfo('000-000-000', '000-000-000', 'mail@mail.com')
    timezone = Timezone('-3:30', 'Newfoundland')
    coordinates = Coordinates(25.4, 25.4)
    nat = Nat("CH")
    location = Location('street', 'city', 'state', 'postcode', coordinates,
                        timezone, nat)
    personal_id = PersonalId('name', 'value')
    login_info = LoginInfo('uuid', 'user', 'password', 'salt', 'md5', 'sha1',
                           'sha256', date.fromisoformat('1997-01-01'))
    user = User(person=person, contact_info=contact_info, location=location,
                personal_id=personal_id, login_info=login_info)

    yield user
