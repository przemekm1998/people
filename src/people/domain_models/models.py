""" Domain models used throughout the app """

import datetime
import re
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class User:
    person: 'Person'
    location: 'Location'
    login_info: 'LoginInfo'
    contact_info: 'ContactInfo'
    personal_id: 'PersonalId'


class Person:
    """ Class to keep track of every person info """

    def __init__(self, gender: str, title: str, first_name: str, second_name: str,
                 date_of_birth: datetime.date):
        self.gender = gender
        self.title = title
        self.first_name = first_name
        self.second_name = second_name
        self.date_of_birth = date_of_birth

    @property
    def age(self) -> int:
        return self._calculate_age()

    @property
    def days_to_birthday(self) -> int:
        return self._days_to_birthday()

    def _calculate_age(self) -> int:
        """
        Calculate years from self date until today
        :return years: Years difference
        """

        today = datetime.date.today()
        years = today.year - self.date_of_birth.year - ((today.month, today.day) < (
            self.date_of_birth.month, self.date_of_birth.day))

        return years

    def _days_to_birthday(self):
        today = datetime.date.today()

        if self._had_birthday_this_year(today):
            birthday_year = today.year + 1
        else:
            birthday_year = today.year

        birthday_date = datetime.date(birthday_year, self.date_of_birth.month,
                                      self.date_of_birth.day)

        return (birthday_date - today).days

    def _had_birthday_this_year(self, today: datetime.date) -> bool:
        """
        Check if anniversary already happened this year
        :param today: Today's date
        :return: True if anniversary already happened this year
        """

        return (
                (today.month == self.date_of_birth.month and
                 today.day > self.date_of_birth.day) or
                (today.month > self.date_of_birth.month)
        )


class LoginInfo:
    """ Composition of data needed for single user """

    REGEX_RULES = (
        dict(rule='[a-z]+', points=1),  # At least one smaller-case letter
        dict(rule='[A-Z]+', points=2),  # At least one upper-case letter
        dict(rule='[0-9]+', points=1),  # At least one number
        dict(rule='.{8,}', points=5),  # At least 8 characters
        dict(rule='[!@#$%^&*(),.?\":{}|<>]', points=3)  # At least one special char
    )

    def __init__(self, uuid: str, username: str, password: str, salt: str, md5: str,
                 sha1: str, sha256: str, date_registered: datetime.date):
        self.uuid = uuid
        self.username = username
        self.password = password
        self.salt = salt
        self.md5 = md5
        self.sha1 = sha1
        self.sha256 = sha256
        self.date_registered = date_registered

    @property
    def password_strength(self) -> int:
        """ Calculate password strength """

        strength = 0

        for pattern in self.REGEX_RULES:
            strength += self._give_points_if_password_matches_regex(pattern)

        return strength

    def _give_points_if_password_matches_regex(self, pattern: Dict[str, Any]) -> int:
        """
        Checking if password matches given regex expression
        :param pattern: Regex pattern to check
        :return: 0 if no match or points for a given rule if regex rule match password
        """

        regex_expression = re.compile(pattern['rule'])
        if regex_expression.search(self.password):
            return pattern['points']
        else:
            return 0


class ContactInfo:
    """ Class to store contact information """

    def __init__(self, phone: str, cell: str, email: str):
        self.phone = phone
        self.cell = cell
        self.email = email

    @property
    def phone(self) -> str:
        return self._phone_num

    @phone.setter
    def phone(self, new_num: str):
        self._phone_num = self._clear_special_chars(new_num)

    @property
    def cell(self) -> str:
        return self._cell_num

    @cell.setter
    def cell(self, new_num: str):
        self._cell_num = self._clear_special_chars(new_num)

    @staticmethod
    def _clear_special_chars(new_num: str, char: str = '-'):
        clear_num = new_num.replace(char, '')
        return clear_num


@dataclass
class Location:
    """ Class to store location information """

    street: str
    city: str
    state: str
    postcode: str
    coordinates: 'Coordinates'
    timezone: 'Timezone'
    nat: 'Nat'


@dataclass
class Coordinates:
    """ Class to store info about coordinates """

    latitude: float
    longitude: float


@dataclass
class Timezone:
    """ Class to store info about timezone """

    offset: str
    description: str


@dataclass
class PersonalId:
    """ Class to store information about id """

    name: str
    value: str


@dataclass()
class Nat:
    """ Class to store NAT """

    name: str
