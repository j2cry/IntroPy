from abc import ABCMeta
from typing import final


@final
class Parameter:
    __read_only = set()
    __primary = set()
    __additional = set()

    __categories = {'read_only': __read_only,
                    'primary': __primary,
                    'additional': __additional}

    # @staticmethod
    # def handler(obj, value):
    #     """ Universal setter """
    #     setattr(obj, '_' + value[0], value[1])

    @classmethod
    def get_set(cls, category: str):
        """ Get specified category of parameters """
        predefined = {param_name for params in cls.__categories.values() for param_name in params}
        return cls.__categories.get(category) if category else predefined

    @classmethod
    def read_only(cls, func):
        cls.__read_only.add(func.__name__)
        return func

    @classmethod
    def primary(cls, func):
        cls.__primary.add(func.__name__)
        return property(func)

    @classmethod
    def additional(cls, func):
        cls.__additional.add(func.__name__)
        return property(func)


class Product(metaclass=ABCMeta):
    """ Base class for products in storage
        New defined parameter keys must be protected! Getter must be decorated with @Parameter.(...) """

    _value_not_defined = 'not defined'

    def __init__(self, **parameters):
        self.__parameters = {}
        # set read_only parameters
        serial = {'serial': parameters.get('serial') if 'serial' in parameters.keys() else self.__hash__()}
        self.__parameters.update(serial)

        # initialize parameters
        predefined = {param_name: value if value else self._value_not_defined
                      for param_name, value in self.get_parameters().items() if param_name not in parameters}
        self.update_parameters(**predefined | parameters)

    def __str__(self):
        """ Get product info card """
        nl = '\n'
        # primary parameters
        location = self._print_parameter(self.location)
        serial = self._print_parameter(self.serial)
        size = self._print_parameter(self.size, lambda res: ' x '.join([str(value) for value in res]))
        mass = self._print_parameter(self.mass)

        parameters = [f'  {param_name.replace("_", " ")}: {value}'
                      f'{" !" if param_name in self.get_parameters("additional").keys() else ""}'
                      for param_name, value in self.__parameters.items()
                      if param_name not in self.get_parameters("primary").keys()
                      and value != self._value_not_defined]

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

    def _print_parameter(self, param_name, action=None):
        """ Get formatted parameter. If parameter not exists return default 'not defined' value """
        if param_name and param_name != self._value_not_defined:
            return action(param_name) if action else param_name
        else:
            return self._value_not_defined

    def _save_predefined_parameters(self):
        """ Save parameters from dict to locals """
        for param_name in self.get_parameters().keys():
            setattr(self, '_' + param_name, self.__parameters.get(param_name))
            # setattr(self, param_name, [param_name, self.__parameters.get(param_name)])

    def update_parameters(self, **parameters):
        """ Add & Update parameters dict with new dict and locals """
        self.__parameters.update({param_name: value for param_name, value in parameters.items()
                                  if param_name not in self.get_parameters("read_only").keys()})    # add new params
        self._save_predefined_parameters()  # save predefined params

    def remove_parameters(self, *parameters: str):
        """ Remove specified parameters from dict. Predefined parameters set to default not-defined """
        for param_name in parameters:
            if param_name not in self.get_parameters('read_only').keys():
                if param_name in self.get_parameters().keys():
                    self.__parameters[param_name] = self._value_not_defined
                    self._save_predefined_parameters()
                else:
                    self.__parameters.pop(param_name, None)

    def get_parameters(self, category: str = None):
        """ Get parameters in specified category. Return JUST PREDEFINED parameters if category is not specified!
            To get ALL actual parameters use 'all' category """
        return {param_name: getattr(self, param_name) for param_name in Parameter.get_set(category)
                if hasattr(self, param_name)} if category != 'all' else self.__parameters

    # predefined attributes
    _location, _serial, _mass, _size, _warranty = '', '', '', '', ''

    @Parameter.primary
    def location(self):
        return self._location

    @Parameter.primary
    @Parameter.read_only
    def serial(self):
        return self._serial

    @Parameter.primary
    def mass(self):
        return self._mass

    @Parameter.primary
    def size(self):
        return self._size

    @Parameter.additional
    def warranty(self):
        return self._warranty
    # ----------------


class Printer(Product):
    _conditions = Product._value_not_defined

    @Parameter.additional
    def conditions(self):
        return self._conditions

    def _additional_output(self, source: str):
        return f'[ Here might be some your info (C) {self.__class__.__name__} class]'


class Scanner(Product):
    pass


class CopyMachine(Product):
    pass


if __name__ == '__main__':
    prod1 = Printer(mass=90, size=(0.3, 0.4, 0.22), serial='serial')
    print('Object created:', prod1, sep='\n')
    prod1.update_parameters(serial='HX92', location='A3-73', conditions='Do not freeze')
    print('Parameters added:', prod1, sep='\n')
    prod1.update_parameters(serial='HX92A37-14', location='A7-19', warranty='2 years')
    print('Parameters updated:', prod1, sep='\n')
    prod1.remove_parameters('conditions', 'mass', 'serial')
    print('Parameters removed:', prod1, sep='\n')

    print(prod1.get_parameters('all'))
