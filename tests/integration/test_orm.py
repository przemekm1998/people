import pytest

from src.people.domain_models.models import User, Person, LoginInfo, ContactInfo, \
    Timezone, Coordinates, Location, PersonalId


@pytest.fixture(scope='function')
def user_fixture(session):
    user = User(date_registered='1993-08-01', nat='nat')
    session.add(user)

    yield user


def test_user_mapper_with_person(session, user_fixture):
    person = Person('male', 'Mr', 'John', 'Doe', '1993-08-01', user_fixture)
    session.add(person)
    session.commit()

    user = session.query(User).one()

    assert user.person.gender == person.gender
    assert user.person.title == person.title
    assert user.person.first_name == person.first_name
    assert user.person.second_name == person.second_name
    assert user.person.date_of_birth == person.date_of_birth
    assert user.person.age == person.age
    assert user.person.date_of_birth == person.date_of_birth


def test_user_mapper_with_login_info(session, user_fixture):
    login_info = LoginInfo('uuid', 'username', 'password', 'salt', 'md5', 'sha1',
                           'sha256', user_fixture)
    session.add(login_info)
    session.commit()

    user = session.query(User).one()
    assert user.login_info.uuid == login_info.uuid
    assert user.login_info.username == login_info.username
    assert user.login_info.password == login_info.password
    assert user.login_info.salt == login_info.salt
    assert user.login_info.md5 == login_info.md5
    assert user.login_info.sha1 == login_info.sha1
    assert user.login_info.sha256 == login_info.sha256
    assert user.login_info.password_strength == login_info.password_strength


def test_user_mapper_with_contact_info(session, user_fixture):
    contact_info = ContactInfo('512-000-000', '000-000-000', 'mail@mail.com',
                               user_fixture)
    session.add(contact_info)
    session.commit()

    user = session.query(User).one()
    assert user.contact_info.phone == contact_info.phone
    assert user.contact_info.cell == contact_info.cell
    assert user.contact_info.email == contact_info.email


def test_location_mapper_with_timezone_and_coordinates(session, user_fixture):
    timezone = Timezone('-3:30', 'Newfoundland')
    coordinates = Coordinates(25.4, 25.4)
    location = Location('street', 'city', 'state', 'postcode', coordinates, timezone,
                        user_fixture)
    session.add(timezone)
    session.add(coordinates)
    session.add(location)
    session.commit()

    user = session.query(User).one()
    assert user.location.street == location.street
    assert user.location.city == location.city
    assert user.location.state == location.state
    assert user.location.postcode == location.postcode
    assert user.location.coordinates == location.coordinates
    assert user.location.timezone == location.timezone


def test_coordination_mapper_can_have_multiple_locations(session, user_fixture):
    timezone = Timezone('-3:30', 'Newfoundland')
    coordinates = Coordinates(25.4, 25.4)
    location_1 = Location('street', 'city', 'state', 'postcode', coordinates, timezone,
                          user_fixture)
    location_2 = Location('street2', 'cit2', 'stat2', 'postcode2', coordinates,
                          timezone, user_fixture)

    session.add(timezone)
    session.add(coordinates)
    session.add(location_1)
    session.add(location_2)
    session.commit()

    coordinates = session.query(Coordinates).one()
    timezone = session.query(Timezone).one()
    assert coordinates.locations == [location_1, location_2]
    assert timezone.locations == [location_1, location_2]


def test_user_mapper_with_personal_id(session, user_fixture):
    personal_id = PersonalId('name', 'value', user_fixture)
    session.add(personal_id)
    session.commit()

    user = session.query(User).one()
    assert user.personal_id.name == personal_id.name
    assert user.personal_id.value == personal_id.value
