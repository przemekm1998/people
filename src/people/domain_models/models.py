""" Domain models used throughout the app """

import datetime
import re
from dataclasses import dataclass
from typing import Dict, Any

from src.people.domain_models.exceptions import ModelCreationException


class User:
    """ Composition of data needed for single user """

    def __init__(self, person: 'Person', location: 'Location',
                 login_info: 'LoginInfo', contact_info: 'ContactInfo',
                 date_registered: str, personal_id: 'PersonalId', nat: str):
        self.person = person
        self.location = location
        self.login_info = login_info
        self.contact_info = contact_info
        self.date_registered = Date(date_registered)
        self.personal_id = personal_id
        self.nat = nat


class Person:
    """ Class to keep track of every person info """

    def __init__(self, gender: str, name: 'Name', date_of_birth: str):
        self.gender = gender
        self.name = name
        self.date_of_birth = Date(date_of_birth)

    @property
    def age(self) -> int:
        return self.date_of_birth.calculate_age()

    @property
    def days_to_birthday(self) -> int:
        return self.date_of_birth.days_to_anniversary()


class Date:
    """ Class to store info about dates """

    def __init__(self, date_str: str):
        self.date = date_str

    @property
    def date(self) -> datetime.date:
        return self._date

    @date.setter
    def date(self, new_date: str):
        self._convert_to_date(new_date)

    def _convert_to_date(self, new_date: str):
        try:
            self._date = datetime.date.fromisoformat(new_date)
        except ValueError:
            raise ModelCreationException(f"Inappropriate date format given: "
                                         f"{new_date}, need ISO format")

    @property
    def day(self) -> int:
        return self.date.day

    @property
    def month(self) -> int:
        return self.date.month

    @property
    def year(self) -> int:
        return self.date.year

    def calculate_age(self) -> int:
        """
        Calculate years from self date until today
        :return years: Years difference
        """

        today = datetime.date.today()

        years = today.year - self.year - ((today.month, today.day) < (self.month,
                                                                      self.day))

        return years

    def days_to_anniversary(self) -> int:
        """ Calculate days left to anniversary """

        today = datetime.date.today()

        if self._had_anniversary_this_year(today):
            anniversary_year = today.year + 1
        else:
            anniversary_year = today.year

        anniversary_date = datetime.date(anniversary_year, self.date.month,
                                         self.date.day)

        return (anniversary_date - today).days

    def _had_anniversary_this_year(self, today: datetime.date) -> bool:
        """
        Check if anniversary already happened this year
        :param today: Today's date
        :return: True if anniversary already happened this year
        """

        return (
                (today.month == self.date.month and
                 today.day > self.date.day) or
                (today.month > self.date.month)
        )

    def __eq__(self, other: 'Date'):
        return self.date == other.date

@dataclass
class Name:
    """ Class to store name information """

    title: str
    first_name: str
    second_name: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> 'Name':
        """
        Generate class instance from dictionary
        :param dictionary: Dictionary with information to instantiate class
        :return: Instance of class
        """

        try:
            return cls(
                title=dictionary['title'],
                first_name=dictionary['first_name'],
                second_name=dictionary['second_name']
            )
        except KeyError:
            raise ModelCreationException("Name information not complete")


@dataclass
class LoginInfo:
    """ Class to store login information """

    REGEX_RULES = (
        dict(rule='[a-z]+', points=1),  # At least one smaller-case letter
        dict(rule='[A-Z]+', points=2),  # At least one upper-case letter
        dict(rule='[0-9]+', points=1),  # At least one number
        dict(rule='.{8,}', points=5),  # At least 8 characters
        dict(rule='[!@#$%^&*(),.?\":{}|<>]', points=3)  # At least one special char
    )

    uuid: str
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str

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

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> 'LoginInfo':
        """
        Generate class instance from dictionary
        :param dictionary: Dictionary with information to instantiate class
        :return: Instance of class
        """

        try:
            return cls(
                uuid=dictionary['uuid'],
                username=dictionary['username'],
                password=dictionary['password'],
                salt=dictionary['salt'],
                md5=dictionary['md5'],
                sha1=dictionary['sha1'],
                sha256=dictionary['sha256']
            )
        except KeyError:
            raise ModelCreationException('LoginInfo information not complete')


class PhoneNumber:
    """ Class to store and correctly parse phone numbers """

    def __init__(self, phone_num: str):
        self.number = phone_num

    @property
    def number(self) -> str:
        return self._phone_num

    @number.setter
    def number(self, new_num: str):
        self._set_number(new_num)

    def _set_number(self, new_num: str):
        self._phone_num = new_num.replace('-', '')

    def __repr__(self) -> str:
        return self.number


@dataclass
class ContactInfo:
    """ Class to store contact information """

    phone: PhoneNumber
    cell: PhoneNumber
    email: str


@dataclass
class Location:
    """ Class to store location information """

    street: str
    city: str
    state: str
    postcode: str
    coordinates: 'Coordinates'
    timezone: 'Timezone'

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]):
        coordinates = Coordinates.from_dict(dictionary['coordinates'])
        timezone = Timezone.from_dict(dictionary['timezone'])
        try:
            return cls(
                street=dictionary['street'],
                city=dictionary['city'],
                state=dictionary['state'],
                postcode=dictionary['postcode'],
                coordinates=coordinates,
                timezone=timezone
            )
        except KeyError:
            raise ModelCreationException("Location info not complete")


@dataclass
class Coordinates:
    """ Class to store info about coordinates """

    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]):
        """
        Generate class instance from dictionary
        :param dictionary: Dictionary with information to instantiate class
        :return: Instance of class
        """

        float_cords = Coordinates._convert_cords_from_str_to_float(dictionary)

        return cls(
            latitude=float_cords['latitude'],
            longitude=float_cords['longitude']
        )

    @staticmethod
    def _convert_cords_from_str_to_float(dictionary: Dict[str, str]) \
            -> Dict[str, float]:
        """
        Converting string values from dict to float
        :param dictionary: Dictionary with coordinates info
        :return: New dictionary with flaot coordinates
        """

        float_cords = dict()
        try:
            float_cords['latitude'] = float(dictionary['latitude'])
            float_cords['longitude'] = float(dictionary['longitude'])

            return float_cords
        except ValueError as err:
            raise ModelCreationException(
                f"Inappropriate coordinates format {str(err)}")
        except KeyError as err:
            raise ModelCreationException(f'Coordinates info not complete: {str(err)}')


@dataclass
class Timezone:
    """ Class to store info about timezone """

    offset: str
    description: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]):
        """
        Generate class instance from dictionary
        :param dictionary: Dictionary with information to instantiate class
        :return: Instance of class
        """

        try:
            return cls(
                offset=dictionary['offset'],
                description=dictionary['description']
            )
        except KeyError as err:
            raise ModelCreationException(f'Timezone info not complete: {str(err)}')


@dataclass
class PersonalId:
    """ Class to store information about id """

    name: str
    value: str

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> 'PersonalId':
        """
        Generate class instance from dictionary
        :param dictionary: Dictionary with information to instantiate class
        :return: Instance of class
        """

        try:
            return cls(
                name=dictionary['name'],
                value=dictionary['value']
            )
        except KeyError:
            raise ModelCreationException('PersonalId information not complete')
