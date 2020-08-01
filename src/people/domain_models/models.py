""" Domain models used throughout the app """

import datetime


class Person:
    """ Class to keep track of every person info """

    def __init__(self, gender: str, title: str, first_name: str, second_name: str,
                 date_of_birth: datetime.date):
        self.gender = gender
        self.title = title
        self.first_name = first_name
        self.second_name = second_name
        self.date_of_birth = Date(date_of_birth)

    @property
    def age(self):
        return self.date_of_birth.calculate_age()

    @property
    def days_to_birthday(self):
        return self.date_of_birth.days_to_anniversary()


class Date:
    """ Class to store info about dates """

    def __init__(self, date_str: datetime.date):
        self.date = date_str

    @property
    def day(self):
        return self.date.day

    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year

    def calculate_age(self):
        """
        Calculate years from self date until today
        :return years: Years difference
        """

        today = datetime.date.today()

        years = today.year - self.year - ((today.month, today.day) < (self.month,
                                                                      self.day))

        return years

    def days_to_anniversary(self):
        """ Calculate days left to anniversary """

        today = datetime.date.today()

        if self._had_anniversary_this_year(today):
            anniversary_year = today.year + 1
        else:
            anniversary_year = today.year

        anniversary_date = datetime.date(anniversary_year, self.date.month,
                                         self.date.day)

        return (anniversary_date - today).days

    def _had_anniversary_this_year(self, today: datetime.date):
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
