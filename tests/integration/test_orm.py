from src.people.domain_models.models import Name, Location, Coordinates, Timezone


def test_name_mapper_can_load_names(session):
    session.execute(
        'INSERT INTO "names" (title, first_name, second_name) VALUES '
        '("Mr", "John", "Doe"),'
        '("Ms", "Jane", "Doe")'
    )
    expected = [
        Name("Mr", "John", "Doe"),
        Name("Ms", "Jane", "Doe")
    ]
    assert session.query(Name).all() == expected


def test_name_mapper_can_save_names(session):
    new_name = Name("Mr", "John", "Doe")
    session.add(new_name)
    session.commit()

    rows = list(session.execute('SELECT * FROM "names"'))
    assert rows == [(1, "Mr", "John", "Doe")]


def test_location_mapper_can_save_location(session):
    session.execute(
        'INSERT INTO "coordinates" (latitude, longitude) VALUES '
        '(-25.3, 54.78)'
    )
    session.execute(
        'INSERT INTO "timezones" ("offset", description) VALUES '
        '("-3:30", "Newfoundland")'
    )
    session.execute(
        'INSERT INTO "locations" (street, city, state, postcode, coordinates, '
        'timezone) VALUES '
        '("street", "city", "state", "05478", (SELECT id FROM "coordinates" WHERE id '
        '= 1), (SELECT id FROM "timezones" WHERE id = 1))'
    )

    expected_location = [Location("street", "city", "state", "05478", 1, 1)]
    expected_coordinates = [Coordinates(latitude=-25.3, longitude=54.78)]
    expected_timezone = [Timezone(offset="-3:30", description="Newfoundland")]

    assert session.query(Location).all() == expected_location
    assert session.query(Timezone).all() == expected_timezone
    assert session.query(Coordinates).all() == expected_coordinates


def test_location_mapper_can_save_locationss(session):
    new_coordinates = Coordinates(latitude=-25.3, longitude=54.78)
    new_timezone = Timezone(offset="-3:30", description="Newfoundland")
    new_location = Location("street", "city", "state", "05478", 1, 1)

    session.add(new_coordinates)
    session.add(new_timezone)
    session.add(new_location)
    session.commit()

    locations_rows = list(session.execute('SELECT * FROM "locations"'))
    timezone_rows = list(session.execute('SELECT * FROM "timezones"'))
    coordinates_rows = list(session.execute('SELECT * FROM "coordinates"'))

    assert locations_rows == [(1, "street", "city", "state", "05478", 1, 1)]
    assert timezone_rows == [(1, "-3:30", "Newfoundland")]
    assert coordinates_rows == [(1, -25.3, 54.78)]
