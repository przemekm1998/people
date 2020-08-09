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
def person_factory_fixture():
    def _make_person(gender='male', title='mr', first_name='john', second_name='doe',
                     date_of_birth=date.fromisoformat('1997-01-01')):
        person = Person(gender, title, first_name, second_name, date_of_birth)
        return person

    return _make_person


@pytest.fixture(scope='function')
def contact_info_factory_fixture():
    def _make_contact(phone='000-000-000', cell='000-000-000', email='mail@mail.com'):
        contact = ContactInfo(phone, cell, email)
        return contact

    return _make_contact


@pytest.fixture(scope='function')
def login_info_factory_fixture():
    def _make_login_info(uuid='uuid', username='user', password='password',
                         salt='salt', md5='md5', sha1='sha1', sha256='sha256',
                         date_registered=date.fromisoformat('1997-01-01')):
        login_info = LoginInfo(uuid, username, password, salt, md5, sha1,
                               sha256, date_registered)
        return login_info

    return _make_login_info


@pytest.fixture(scope='function')
def personal_id_factory_fixture():
    def _make_id(name='name', value='value'):
        personal_id = PersonalId(name, value)

        return personal_id

    return _make_id


@pytest.fixture(scope='function')
def nat_factory_fixture():
    def _make_nat(name="CH"):
        nat = Nat(name)
        return nat

    return _make_nat


@pytest.fixture(scope='function')
def timezone_factory_fixture(offset='-3:30', description='Newfoundland'):
    def _make_timezone():
        timezone = Timezone(offset, description)
        return timezone

    return _make_timezone


@pytest.fixture(scope='function')
def coordinates_factory_fixture():
    def _make_coordinates(latitude=25.4, longitude=25.4):
        coordinates = Coordinates(latitude, longitude)
        return coordinates

    return _make_coordinates


@pytest.fixture(scope='function')
def location_factory_fixture(nat_factory_fixture, timezone_factory_fixture,
                             coordinates_factory_fixture):
    def _make_location(street='street', city='city', state='state',
                       postcode='postcode',
                       coordinates=coordinates_factory_fixture(),
                       timezone=timezone_factory_fixture(),
                       nat=nat_factory_fixture()):
        location = Location(street, city, state, postcode, coordinates,
                            timezone, nat)
        return location

    return _make_location


@pytest.fixture(scope='function')
def user_factory_fixture(person_factory_fixture, contact_info_factory_fixture,
                         login_info_factory_fixture, personal_id_factory_fixture,
                         location_factory_fixture):
    def _make_user(person=person_factory_fixture(),
                   contact_info=contact_info_factory_fixture(),
                   login_info=login_info_factory_fixture(),
                   personal_id=personal_id_factory_fixture(),
                   location=location_factory_fixture()):
        person = person
        contact_info = contact_info
        login_info = login_info
        personal_id = personal_id
        location = location
        user = User(person=person, contact_info=contact_info, location=location,
                    personal_id=personal_id, login_info=login_info)

        return user

    yield _make_user
