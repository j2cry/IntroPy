from random import random, randint, choice, choices
from string import ascii_letters, digits, punctuation
from collections.abc import Iterable


class DataRandom:
    symbols = ascii_letters + digits + punctuation

    NUMERIC = (int, float)
    SIMPLE_WITHOUT_NONE = (int, float, str, bool)
    WITHOUT_COLLECTIONS = (int, float, str, bool, None)

    def __init__(self, int_bundle=(-1, 1), float_bundle=(-1, 1), round_digits=3, length=8, nested_level=1, elem_count=5,
                 nested_elem_count=10, types=NUMERIC):
        """ Initialize randomization object with defaults or selected parameters """
        try:
            self.__int_bundle = (min(int_bundle), max(int_bundle))
        except TypeError:
            self.__int_bundle = (-1, 1)

        try:
            self.__float_bundle = (min(float_bundle), max(float_bundle))
        except TypeError:
            self.__float_bundle = (-1, 1)

        self.__rd = round_digits
        self.__ln = length
        self.__level = nested_level
        self.__count = elem_count
        self.__nested_count = nested_elem_count
        self.__types = types if isinstance(types, Iterable) else [types]

    def set_param(self, int_bundle=None, float_bundle=None, round_digits=None, length=None, nested_level=None,
                  elem_count=None, nested_elem_count=None, types=None):
        """ Modify randomization parameters """
        try:
            self.__int_bundle = (min(int_bundle), max(int_bundle)) if int_bundle else self.__int_bundle
        except TypeError:
            pass

        try:
            self.__float_bundle = (min(float_bundle), max(float_bundle)) if float_bundle else self.__float_bundle
        except TypeError:
            pass

        self.__float_bundle = (min(float_bundle), max(float_bundle)) if float_bundle else self.__float_bundle
        self.__rd = round_digits if round_digits else self.__rd
        self.__ln = length if length else self.__ln
        self.__level = nested_level if nested_level else self.__level
        self.__count = elem_count if elem_count else self.__count
        self.__nested_count = nested_elem_count if nested_elem_count else self.__nested_count

        types = types if isinstance(types, Iterable) else [types]
        self.__types = types if types else self.__types

    @staticmethod
    def random_sign(num):
        """ Set random sign for given numeric """
        if isinstance(num, int) or isinstance(num, float):
            return num if randint(0, 1) else -num
        else:
            return None

    def random_primitive(self):
        """ Returns random value of acceptable type (set in .__types) : int, float, str, bool or None """
        if not self.__types:
            return None

        # Random type of value
        tp = choice(self.__types)
        if tp is int:           # generate int
            r = randint(self.__int_bundle[0], self.__int_bundle[1])
        elif tp is float:       # generate float
            n = randint(self.__float_bundle[0], self.__float_bundle[1])
            r = random()
            r = round(n + r, self.__rd) if n + r <= self.__float_bundle[1] else round(n - r, self.__rd)
        elif tp is str:         # generate str
            r = ''.join(choices(self.symbols, k=self.__ln))
        elif tp is bool:        # generate bool
            r = bool(randint(0, 1))
        elif tp is None:        # generate NoneType
            r = None
        else:                   # you can add your own class here
            r = None
        return r

    def random_list(self, nested=False):
        """ Returns list of random values with nested lists according to nesting level;
            level=0 returns list with primitives (int, float, str, bool or None) """
        res = []
        # checking if is running for nested
        items_count = self.__nested_count if nested else self.__count
        for i in range(items_count):
            if self.__level:
                self.__level -= 1
                res.append(self.random_list(True))
                self.__level += 1
            else:
                res.append(self.random_primitive())
        return res

    def generator(self, nested=False):
        """ Returns generator of random values with nested lists according to nesting level;
            level=0 returns list with primitives (int, float, str, bool or None) """
        # checking if is running for nested
        items_count = self.__nested_count if nested else self.__count
        for i in range(items_count):
            if self.__level:
                self.__level -= 1
                yield self.random_list(True)
                self.__level += 1
            else:
                yield self.random_primitive()
