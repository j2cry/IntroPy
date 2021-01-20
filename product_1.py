from abc import ABCMeta
from typing import Final


class Product(metaclass=ABCMeta):
    """ Base class for products in storage. """

    _value_not_defined: Final = 'not defined'          # default not-defined value

    # parameters containers
    # set можно заменить на dict, тогда можно будет задать начальные значения как во 2ом варианте, но не вижу смысла
    _read_only = {'serial'}
    _primary = {'location', 'serial', 'mass', 'size'}
    _additional = {'warranty'}

    # _predefined = _primary | _additional
    __categories = {'read_only': _read_only,
                    'primary': _primary,
                    'additional': _additional}

    def __new__(cls, *args, **kwargs):
        """ Constructor for collecting parameter containers from all class tree: child --> parent """
        cls._predefined = set()
        for category_name in cls.__categories.keys():
            container = set()
            for parent_class in cls.mro():
                container |= getattr(parent_class, '_' + category_name, set())
            setattr(cls, '_' + category_name, container)
            # collect _predefined container
            cls._predefined |= container if category_name != 'read_only' else set()
        return super(Product, cls).__new__(cls)

    def __init__(self, **parameters):
        if 'serial' not in parameters.keys():
            parameters |= {'serial': self.__hash__()}
        # initialize parameters
        predefined = {param_name: self._value_not_defined for param_name in self._predefined}
        self.__parameters = {}
        self.update_parameters(**predefined | parameters)

    def __str__(self):
        """ Get product info card """
        nl = '\n'
        # primary parameters
        location = self._print_parameter(self.__parameters.get('location'))
        serial = self._print_parameter(self.__parameters.get('serial'))
        size = self._print_parameter(self.__parameters.get('size'),
                                     lambda res: ' x '.join([str(value) for value in res]))
        mass = self._print_parameter(self.__parameters.get('mass'))

        parameters = [f'  {param_name.replace("_", " ")}: {value}{" !" if param_name in self._additional else ""}'
                      for param_name, value in self.__parameters.items()
                      if param_name not in self._primary and value != self._value_not_defined]

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

    def update_parameters(self, **parameters):
        """ Add & Update parameters dict with new dict and locals """
        self.__parameters.update(parameters)    # add new params

    def remove_parameters(self, *parameters):
        """ Remove specified parameters from dict. Predefined parameters set to default not-defined """
        for param_name in parameters:
            if param_name not in self._read_only:
                if param_name in self._predefined:
                    self.__parameters[param_name] = self._value_not_defined
                else:
                    self.__parameters.pop(param_name, None)

    def get_parameters(self, category: str = None):
        """ Get parameters in specified category. Return JUST PREDEFINED parameters if category is not specified!
            To get ALL actual parameters use 'all' category """
        # это просто ради одинаковости интерфейса с вариантом 2
        return {param_name: value for param_name, value in self.__parameters.items()
                if param_name in self.__categories.get(category)} if category != 'all' else self.__parameters


class Printer(Product):
    _additional = {'conditions'}

    def _additional_output(self, source: str):
        return f'[ Here might be some your info (C) {self.__class__.__name__} class]'


class Scanner(Product):
    pass


class CopyMachine(Product):
    pass


if __name__ == '__main__':
    prod1 = Printer(mass=90, size=(0.3, 0.4, 0.22))
    print('Object created:', prod1, sep='\n')
    prod1.update_parameters(serial='HX92', location='A3-73', conditions='Do not freeze')
    print('Parameters added:', prod1, sep='\n')
    prod1.update_parameters(serial='HX92A37-14', location='A7-19', warranty='2 years')
    print('Parameters updated:', prod1, sep='\n')
    prod1.remove_parameters('conditions', 'mass', 'serial')
    print('Parameters removed:', prod1, sep='\n')

    print(prod1.get_parameters('all'))
