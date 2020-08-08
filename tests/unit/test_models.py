from datetime import date
from unittest import mock

import pytest

from src.people.domain_models.models import Person, ContactInfo, LoginInfo


class FakeDate(date):

    def __new__(cls, *args, **kwargs):
        return date.__new__(date, *args, **kwargs)


class FakePerson(Person):

    def __init__(self, date_of_birth: date):
        self.date_of_birth = date_of_birth


class FakeContactInfo(ContactInfo):

    def __init__(self, phone: str = '000-000-000'):
        self.phone = phone


class FakeLoginInfo(LoginInfo):

    def __init__(self, password: str):
        self.password = password


@mock.patch('src.people.domain_models.models.datetime.date', FakeDate)
@pytest.mark.parametrize('date_1, age', [
    (date.fromisoformat('1993-07-20'), 27),
    (date.fromisoformat('2020-07-20'), 0),
])
def test_person_age(date_1, age):
    FakeDate.today = classmethod(lambda cls: date(2020, 7, 31))
    person = FakePerson(date_1)
    assert age == person.age


@mock.patch('src.people.domain_models.models.datetime.date', FakeDate)
@pytest.mark.parametrize('date_1, expected_days_to_birthday', [
    (date.fromisoformat('1993-08-01'), 1),
    (date.fromisoformat('1993-07-31'), 0),
    (date.fromisoformat('1993-07-30'), 364),
])
def test_person_days_to_birthday(date_1, expected_days_to_birthday):
    FakeDate.today = classmethod(lambda cls: date(2020, 7, 31))
    person = FakePerson(date_of_birth=date_1)
    assert person.days_to_birthday == expected_days_to_birthday


@pytest.mark.parametrize('password, points', [
    ('supertajne', 6),  # Lower-case and 8+ chars
    ('Ab1337', 4),  # Upper-case, lower-case and number
    ('Ab133785', 9),  # Upper-case, lower-case, number, 8+ chars
    ('Ab133785%', 12),  # All rules match
    ('', 0)
])
def test_login_info_password_strength(password, points):
    user = FakeLoginInfo(password=password)

    assert user.password_strength == points


def test_contact_info_remove_dashes_from_phone_number():
    contact_info = FakeContactInfo('012-324-548')

    assert contact_info.phone == '012324548'
