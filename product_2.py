from abc import ABCMeta
from typing import final


@final
class Parameter:
    __primary_params = set()
    __additional_params = set()

    __categories = {'primary': __primary_params,
                    'additional': __additional_params}

    # @staticmethod
    # def handler(obj, value):
    #     """ Universal setter """
    #     setattr(obj, '_' + value[0], value[1])

    @classmethod
    def get_set(cls, category: str):
        """ Get specified category of parameters """
        all_params = {param_name for params in cls.__categories.values() for param_name in params}
        return cls.__categories.get(category) if category else all_params

    @classmethod
    def primary(cls, func):
        cls.__primary_params.add(func.__name__)
        return property(func)

    @classmethod
    def additional(cls, func):
        cls.__additional_params.add(func.__name__)
        return property(func)


class Product(metaclass=ABCMeta):
    """ Base class for products in storage
        New defined parameter keys must be protected! Getter must be decorated with @Parameter.(...) """

    parameter = Parameter()
    _value_not_defined = 'not defined'

    def __init__(self, **parameters):
        if 'serial' not in parameters.keys():
            parameters |= {'serial': self.__hash__()}
        self.__parameters = {}
        self.update_parameters(**parameters)

    def __str__(self):
        """ Get product info card """
        nl = '\n'
        location = self._get_parameter(self.location)
        serial = self._get_parameter(self.serial)
        size = self._get_parameter(self.size, lambda res: ' x '.join([str(value) for value in res]))
        mass = self._get_parameter(self.mass)

        parameters = [f'  {key.replace("_", " ")}: {value}' \
                      f'{" !" if key in self._get_parameters_set("additional") else ""}'
                      for key, value in self.__parameters.items()
                      if key not in self._get_parameters_set("primary").keys()]

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

    def _get_parameter(self, name, action=None):
        """ Get formatted parameter. If parameter not exists return default 'not defined' value """
        if name and name != self._value_not_defined:
            return action(name) if action else name
        else:
            return self._value_not_defined

    def _get_parameters_set(self, category: str = None):
        """ Get specified parameters in specified category """
        return {name: getattr(self, name) for name in self.parameter.get_set(category) if hasattr(self, name)}

    def _save_base_parameters(self):
        """ Save parameters from dict to locals """
        for param in self._get_parameters_set():
            setattr(self, '_' + param, self.__parameters.get(param))
            # setattr(self, param, [param, self.__parameters.get(param)])

    def update_parameters(self, **parameters):
        """ Add & Update parameters dict with new dict and locals """
        self.__parameters.update(parameters)  # add new params
        # add unset base params
        params = {name: getattr(self, name) for name in self._get_parameters_set() if name not in parameters}
        self.__parameters.update(params)
        self._save_base_parameters()  # save predefined params

    def remove_parameters(self, *parameters: str):
        """ Remove specified parameters from dict. Predefined parameters set to default not-defined """
        for key in parameters:
            if key in self._get_parameters_set():
                self.__parameters[key] = self._value_not_defined
            else:
                self.__parameters.pop(key, None)
        self._save_base_parameters()

    # Вся вот эта катавась только ради того, чтобы управлять объектом через
    # Product.update_parameters и Product.remove_parameters

    # predefined attributes
    _location, _serial, _mass, _size = '', '', '', ''

    @parameter.primary
    def location(self):
        return self._location

    @parameter.primary
    def serial(self):
        return self._serial

    @parameter.primary
    def mass(self):
        return self._mass

    @parameter.primary
    def size(self):
        return self._size
    # ----------------


class Printer(Product):
    _conditions = 'Do not freeze'

    @Parameter.additional
    def conditions(self):
        return self._conditions

    def _additional_output(self, source: str):
        # return f'PRINTER PREDEFINED PARAMETERS: {self._get_parameter(self.conditions)}'
        return ''


class Scanner(Product):
    pass


class CopyMachine(Product):
    pass


prod1 = Printer(mass=90, size=(0.3, 0.4, 0.22))
prod2 = Scanner(another='Some information')
prod3 = CopyMachine(serial='HX92', location='A3-73')

prod1.update_parameters(gotcha='Brooklyn')
print(prod1)
prod1.remove_parameters('gotcha', 'mass')
print(prod1)
print(prod2)
print(prod3)
