from abc import ABCMeta, abstractmethod
from typing import Union, Final, final


class Product(metaclass=ABCMeta):
    """ Base class for products in storage """

    _value_not_defined: Final = 'not defined'          # default not-defined value

    # parameters containers     TODO: заменить их на dict?
    _read_only = {'serial'}
    _primary = {'location', 'serial', 'mass', 'size'}
    _additional = {'warranty'}

    _predefined = _primary | _additional
    # _other = set()

    def __init__(self, **parameters):
        self.__parameters = {}
        # adding predefined
        self.__parameters.update({key: self._value_not_defined for key in self._predefined})
        if 'serial' not in parameters.keys():
            parameters |= {'serial': self.__hash__()}
        self.update_parameters(**parameters)

    def __str__(self):
        """ Get product info card """
        nl = '\n'
        # primary parameters
        location = self._print_parameter(self.__parameters.get('location'))
        serial = self._print_parameter(self.__parameters.get('serial'))
        size = self._print_parameter(self.__parameters.get('size'), lambda res: ' x '.join([str(value) for value in res]))
        mass = self._print_parameter(self.__parameters.get('mass'))

        parameters = [f'  {key.replace("_", " ")}: {value}{" !" if key in self._additional else ""}'
                      for key, value in self.__parameters.items()
                      if key not in self._primary and value != self._value_not_defined]

        result = f'Product type: {type(self).__name__}{nl}' \
                 f'S/N: {serial}{nl}' \
                 f'Location: {location}{nl}' \
                 f'Mass: {mass}{nl}' \
                 f'Size: {size}{nl}' \
                 f'Additional information:{nl}'
        result += f'{nl.join(parameters)}{nl}' if parameters else ''
        additional = self._additional_output(result)
        result += additional + nl if additional else ''
        return result

    def _additional_output(self, source: str):
        """ Override it to add something to product info card """
        return ''

    def _print_parameter(self, name, action=None):
        """ Get formatted parameter. If parameter not exists return default 'not defined' value """
        if name and name != self._value_not_defined:
            return action(name) if action else name
        else:
            return self._value_not_defined

    def update_parameters(self, **parameters):
        """ Add & Update parameters dict with new dict and locals """
        # self._other = parameters.keys() - self._predefined    # update container
        self.__parameters.update(parameters)    # add new params

    def remove_parameters(self, *parameters):
        """ Remove specified parameters from dict. Predefined parameters set to default not-defined """
        for key in parameters:
            if key not in self._read_only:
                if key in self._predefined:
                    self.__parameters[key] = self._value_not_defined
                else:
                    self.__parameters.pop(key, None)


class Printer(Product):
    _additional = {'conditions'}
    pass


class Scanner(Product):
    pass


class CopyMachine(Product):
    pass


# prod1 = Printer()
# print(prod1)
# prod1.update_parameters(location='A22', warranty='1 year', shipping_date='13.04.2021')
# print(prod1)
# prod1.remove_parameters('serial', 'location')
# print(prod1)


prod1 = Printer(mass=90, size=(0.3, 0.4, 0.22))
prod2 = Scanner(another='Some information')
prod3 = CopyMachine(serial='HX92', location='A3-73')

prod1.update_parameters(conditions='Brooklyn')
print(prod1)
prod1.remove_parameters('gotcha', 'mass')
print(prod1)
print(prod2)
print(prod3)
