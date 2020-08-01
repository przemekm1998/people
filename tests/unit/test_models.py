from datetime import date
from unittest import mock

import pytest

from src.people.domain_models.models import Person, Date, Name, LoginInfo


class FakeDate(date):

    def __new__(cls, *args, **kwargs):
        return date.__new__(date, *args, **kwargs)


class FakePerson(Person):

    def __init__(self, date_of_birth=date.fromisoformat('1993-07-20')):
        self.date_of_birth = Date(date_of_birth)


@mock.patch('src.people.domain_models.models.datetime.date', FakeDate)
@pytest.mark.parametrize('date_1, date_2, diff', [
    (date.fromisoformat('1993-07-20'), date.fromisoformat('2020-07-30'), 27),
    (date.fromisoformat('2020-07-20'), date.fromisoformat('2020-07-30'), 0),
])
def test_years_difference(date_1, date_2, diff):
    FakeDate.today = classmethod(lambda cls: date(2020, 7, 31))
    date_ = Date(date_1)
    years_diff = date_.calculate_age()
    assert years_diff == diff


@mock.patch('src.people.domain_models.models.datetime.date', FakeDate)
@pytest.mark.parametrize('date_1, expected_days_to_anniversary', [
    (date.fromisoformat('1993-08-01'), 1),
    (date.fromisoformat('1993-07-31'), 0),
    (date.fromisoformat('1993-07-30'), 364),
])
def test_date_anniversary_days_left(date_1, expected_days_to_anniversary):
    FakeDate.today = classmethod(lambda cls: date(2020, 7, 31))
    date_ = Date(date_1)
    assert date_.days_to_anniversary() == expected_days_to_anniversary


@mock.patch('src.people.domain_models.models.datetime.date', FakeDate)
def test_person_age():
    FakeDate.today = classmethod(lambda cls: date(2020, 7, 31))
    date_of_birth = date.fromisoformat('1993-07-20')
    person = FakePerson(date_of_birth=date_of_birth)
    assert person.age == 27


@mock.patch('src.people.domain_models.models.datetime.date', FakeDate)
def test_person_days_until_birthday():
    FakeDate.today = classmethod(lambda cls: date(2020, 7, 31))
    person = FakePerson(date_of_birth=date.fromisoformat('1993-08-01'))
    assert person.days_to_birthday == 1


def test_create_name_from_dict():
    name_info = dict(title='mr', first_name='John', second_name='Doe')
    new_name = Name.from_dict(name_info)

    assert new_name.title == name_info['title']
    assert new_name.first_name == name_info['first_name']
    assert new_name.second_name == name_info['second_name']


@pytest.mark.parametrize('password, points', [
    ('supertajne', 6),  # Lower-case and 8+ chars
    ('Ab1337', 4),  # Upper-case, lower-case and number
    ('Ab133785', 9),  # Upper-case, lower-case, number, 8+ chars
    ('Ab133785%', 12),  # All rules match
    ('', 0)
])
def test_login_info_password_strength(password, points):
    login_info = LoginInfo(uuid='', username='', password=password, salt='', md5='',
                           sha1='', sha256='')

    assert login_info.password_strength == points


def test_login_info_from_dict():
    login_info_dict = dict(uuid='uuid',
                           username='username',
                           password='passwd',
                           salt='salt',
                           md5='md5',
                           sha1='sha1',
                           sha256='sha256')

    login_info = LoginInfo.from_dict(login_info_dict)

    assert login_info.uuid == login_info_dict['uuid']
    assert login_info.username == login_info_dict['username']
    assert login_info.password == login_info_dict['password']
    assert login_info.salt == login_info_dict['salt']
    assert login_info.md5 == login_info_dict['md5']
    assert login_info.sha1 == login_info_dict['sha1']
    assert login_info.sha256 == login_info_dict['sha256']