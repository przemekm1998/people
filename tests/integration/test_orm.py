from datetime import date

import pytest

from src.people.domain_models.models import Person, ContactInfo, \
    Timezone, Coordinates, Location, PersonalId, Nat, User, LoginInfo


def test_user_mapper(session, user_fixture):
    user = user_fixture
    db_user = session.query(User).one()

    assert user == db_user


def test_coordination_mapper_can_have_multiple_locations(session):
    timezone = Timezone('-3:30', 'Newfoundland')
    coordinates = Coordinates(25.4, 25.4)
    nat = Nat("CH")
    location_1 = Location('street', 'city', 'state', 'postcode', coordinates,
                          timezone, nat)
    location_2 = Location('street2', 'cit2', 'stat2', 'postcode2', coordinates,
                          timezone, nat)

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
