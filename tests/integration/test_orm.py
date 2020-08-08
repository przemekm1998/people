from src.people.domain_models.models import Timezone, Coordinates, Location, Nat, User


def test_user_mapper(session, user_fixture):
    user = user_fixture

    session.add(user)
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


def test_coordinates_unique_constraint(session, user_fixture):
    coordinates_1 = Coordinates(25.4, 25.4)
    coordinates_2 = Coordinates(25.4, 25.4)

    user_1 = user_fixture
    user_1.location.coordinates = coordinates_1
    user_2 = user_fixture
    user_2.location.coordaintes = coordinates_2

    session.add(user_1)
    session.add(user_2)
    session.commit()

    coordinates_db = session.query(Coordinates).all()
    assert len(coordinates_db) == 1
    assert coordinates_db[0].longitude == coordinates_1.longitude
    assert coordinates_db[0].latitude == coordinates_1.latitude
