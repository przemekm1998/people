from datetime import date

import pytest

from src.people.domain_models.models import User, Person, ContactInfo, \
    Timezone, Coordinates, Location, PersonalId, Nat


@pytest.fixture(scope='function')
def user_fixture(session):
    user = User('uuid', 'user', 'password', 'salt', 'md5', 'sha1', 'sha256',
                date.fromisoformat('1997-01-01'))
    session.add(user)

    yield user


def test_user_mapper(session):
    user = User('uuid', 'user', 'password', 'salt', 'md5', 'sha1', 'sha256',
                date.fromisoformat('1997-01-01'))
    session.add(user)

    db_user = session.query(User).one()
    assert user == db_user


def test_user_mapper_with_person(session, user_fixture):
    person = Person('male', 'Mr', 'John', 'Doe', date.fromisoformat('1993-08-01'),
                    user_fixture)
    session.add(person)
    session.commit()

    user = session.query(User).one()

    assert user.person == person


def test_user_mapper_with_contact_info(session, user_fixture):
    contact_info = ContactInfo('512-000-000', '000-000-000', 'mail@mail.com',
                               user_fixture)
    session.add(contact_info)
    session.commit()

    user = session.query(User).one()
    assert user.contact_info == contact_info


def test_location_mapper_with_timezone_nat_and_coordinates(session, user_fixture):
    timezone = Timezone('-3:30', 'Newfoundland')
    coordinates = Coordinates(25.4, 25.4)
    nat = Nat("CH")
    location = Location('street', 'city', 'state', 'postcode', coordinates, timezone,
                        nat, user_fixture)
    session.add(timezone)
    session.add(coordinates)
    session.add(nat)
    session.add(location)
    session.commit()

    user = session.query(User).one()
    assert user.location.street == location.street
    assert user.location.city == location.city
    assert user.location.state == location.state
    assert user.location.postcode == location.postcode
    assert user.location.coordinates == location.coordinates
    assert user.location.timezone == location.timezone
    assert user.location.nat == nat


def test_coordination_mapper_can_have_multiple_locations(session, user_fixture):
    timezone = Timezone('-3:30', 'Newfoundland')
    coordinates = Coordinates(25.4, 25.4)
    nat = Nat("CH")
    location_1 = Location('street', 'city', 'state', 'postcode', coordinates,
                          timezone, nat, user_fixture)
    location_2 = Location('street2', 'cit2', 'stat2', 'postcode2', coordinates,
                          timezone, nat, user_fixture)

    session.add(timezone)
    session.add(coordinates)
    session.add(location_1)
    session.add(location_2)
    session.commit()

    coordinates_db = session.query(Coordinates).one()
    timezone_db = session.query(Timezone).one()
    nat_db = session.query(Nat).one()

    assert coordinates_db.locations == [location_1, location_2]
    assert timezone_db.locations == [location_1, location_2]
    assert nat_db.locations == [location_1, location_2]


def test_user_mapper_with_personal_id(session, user_fixture):
    personal_id = PersonalId('name', 'value', user_fixture)
    session.add(personal_id)
    session.commit()

    user = session.query(User).one()
    assert user.personal_id == personal_id
