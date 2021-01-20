from calendar import monthrange
from data_random import DataRandom
from typing import Union
from product_1 import Printer, Scanner, CopyMachine


# 1
class Date:
    """ Format date from str to numeric """
    date = '01-01-1980'

    def __init__(self, date: str):
        """ Set date as string in format dd-mm-yyyy """
        Date.date = date

    @classmethod
    def get(cls):
        try:
            day, month, year = map(int, cls.date.split('-'))
        except ValueError:
            day, month, year = (0, 0, 0)

        return (day, month, year) if all(cls.validate(day, month, year)) else None

    @staticmethod
    def validate(day: int, month: int, year: int) -> (bool, bool, bool):
        """ Validate day, month and year.
            Return tuple of bool with results: (day, month, year) """
        day_valid, month_valid, year_valid = False, False, False
        if year:        # validate year
            year_valid = True

        month_valid = 0 < month < 13
        if month_valid:       # validate month
            weekday, days_count = monthrange(year, month)
            day_valid = (0 < day < days_count + 1)

        return day_valid, month_valid, year_valid


def test_task_1():      # это можно скормить Pytest
    assert Date('0-04-1997').get() is None
    assert Date('29-02-2016').get() == (29, 2, 2016)
    assert Date('29-02-2015').get() is None
    assert Date('31-12-2010').get() == (31, 12, 2010)
    assert Date('17-15-2006').get() is None
    assert Date('5-04-2023').get() == (5, 4, 2023)


# 2
class MeaninglessException(Exception):
    pass


def test_task_2():
    data = DataRandom(int_bundle=(-10, 10), nested_level=1, elem_count=20, nested_elem_count=2, types=int)
    values = data.random_list()

    for a, b in values:
        try:
            if b <= 0:      # set any condition to raise exception
                raise MeaninglessException("Something happened. Go next.")
            else:
                print(round(a / b, 3))

        except MeaninglessException as e:
            print(e)


# 3 немножко не так, как требовалось в задании, но суть не изменилась
class TypeMismatchException(Exception):
    pass


def test_task_3():
    def check_value(val, required_type: type):        # запихнул сюда, чтоб не отсвечивала в основном модуле
        if isinstance(val, required_type) and (not isinstance(val, bool) or required_type is bool):
            return val
        else:
            raise TypeMismatchException

    data = DataRandom(int_bundle=(-10, 10), nested_level=0, elem_count=20, nested_elem_count=1,
                      types=DataRandom.WITHOUT_COLLECTIONS)
    values = data.random_list()
    result = []
    print('source:', values)

    for value in values:
        try:
            result.append(check_value(value, int))
        except TypeMismatchException:
            pass

    print('result:', result)


# 4, 5, 6
class Storage:
    def __init__(self):
        pass

    def add_products(self, *products):
        """ Add products to storage """
        pass

    def del_products(self, *id):
        """ Delete products from storage by it's ID (hash?) """
        pass

    def find_product(self, **parameters):
        """ Find product with specified parameters """
        pass

    def update_product_info(self, id, **parameters):
        """ Update product parameters """
        pass


# 7 для этого вроде бы есть класс Complex в модуле numbers
def same_type(func):        # decorator for value validation
    def wrapper(self, value):
        if isinstance(self, type(value)):
            return func(self, value)
        else:
            return None
    return wrapper


class MyComplex:
    def __init__(self, a: Union[int, float], b: Union[int, float], round_digits=2):
        self.a, self.b = a, b
        self.round_digits = round_digits

    def __str__(self):
        rounded_b = round(self.b, self.round_digits)
        return f'{round(self.a, self.round_digits)} {f"+ {rounded_b}" if self.b > 0 else f"- {abs(rounded_b)}"}i'

    @same_type
    def __add__(self, other):
        new_a, new_b = self.a + other.a, self.b + other.b
        return MyComplex(new_a, new_b, self.round_digits)

    @same_type
    def __sub__(self, other):
        return self + MyComplex(-other.a, -other.b)

    @same_type
    def __mul__(self, other):
        new_a = self.a * other.a - self.b * other.b
        new_b = self.b * other.a + self.a * other.b
        return MyComplex(new_a, new_b, self.round_digits)

    @same_type
    def __truediv__(self, other):
        new_a = (self.a * other.a + self.b * other.b) / (other.a ** 2 + other.b ** 2)
        new_b = (self.b * other.a - self.a * other.b) / (other.a ** 2 + other.b ** 2)
        return MyComplex(new_a, new_b, self.round_digits)


def test_task_7():      # скормить Pytest
    comp_a = MyComplex(4, 5)
    comp_b = MyComplex(2, 3)
    assert str(comp_a + comp_b) == '6 + 8i'
    assert str(comp_a - comp_b) == '2 + 2i'
    assert str(comp_a * comp_b) == '-7 + 22i'
    assert str(comp_a / comp_b) == '1.77 - 0.15i'

    comp_a = MyComplex(3.5, 1.4)
    comp_b = MyComplex(2.1, 3.7)
    assert str(comp_a + comp_b) == '5.6 + 5.1i'
    assert str(comp_a - comp_b) == '1.4 - 2.3i'
    assert str(comp_a * comp_b) == '2.17 + 15.89i'
    assert str(comp_a / comp_b) == '0.69 - 0.55i'


# main
if __name__ == '__main__':
    # tasks = {'1': test_task_1, '2': test_task_2, '3': test_task_3, '4': test_task_4, '5': test_task_5,
    #          '6': test_task_6, '7': test_task_7}
    tasks = {'1': test_task_1, '2': test_task_2, '3': test_task_3, '7': test_task_7}

    running = True
    while running:
        inp = input('> ')
        if inp == 'q':
            running = False
        elif callable(tasks.get(inp)):
            tasks.get(inp)()
