from datetime import date

import pytest

from src.people.domain_models.models import Person, Date


class FakePerson(Person):

    def __init__(self, date_of_birth=date.fromisoformat('1993-07-20')):
        self.date_of_birth = Date(date_of_birth)


@pytest.mark.parametrize('date_1, date_2, diff', [
    (date.fromisoformat('1993-07-20'), date.fromisoformat('2020-07-30'), 27),
    (date.fromisoformat('2020-07-30'), date.fromisoformat('1993-07-20'), 27),
    (date.fromisoformat('2020-07-20'), date.fromisoformat('2020-07-30'), 0),
    (date.fromisoformat('2020-07-30'), date.fromisoformat('2020-07-20'), 0)
])
def test_years_difference(date_1, date_2, diff):
    date_ = Date(date_1)
    years_diff = date_.years_difference(date_2)
    assert years_diff == diff


def test_person_age():
    date_of_birth = date.fromisoformat('1993-07-20')
    person = FakePerson(date_of_birth=date_of_birth)
    assert person.age == 27
