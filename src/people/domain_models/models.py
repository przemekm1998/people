""" Domain models used throughout the app """

from datetime import date


class Person:
    """ Class to keep track of every person info """

    def __init__(self, gender: str, title: str, first_name: str, second_name: str,
                 date_of_birth: date):
        self.gender = gender
        self.title = title
        self.first_name = first_name
        self.second_name = second_name
        self.date_of_birth = Date(date_of_birth)

    @property
    def age(self):
        return self.date_of_birth.years_difference(date.today())


class Date:
    """ Class to store info about dates """

    def __init__(self, date_str: date):
        self._date = date_str

    def years_difference(self, other_date: date):
        """
        Calculate years between two dates
        :param other_date: Another date to count years difference
        :return years: Years difference
        """

        years = self._date.year - other_date.year - (
                (self._date.month, self._date.day) < (other_date.month,
                                                      other_date.day))
        # Case when user gives elder other date than self _date
        if years < 0:
            years = (years * (-1)) - 1

        return years
