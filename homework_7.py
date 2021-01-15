from data_random import DataRandom
from abc import abstractmethod


# 1
class Matrix:
    """ This 2D matrix can contain as numeric so string values """

    def __init__(self, values: list[list], default=None):
        """ Initialize matrix with values (list of lists) """
        self.__default_zero_value = default
        self.__values = [[]]        # indexing: [row][col]
        try:
            self.__rows_count = len(values)     # количество строк
            self.__columns_count = max(map(len, values))       # количество столбцов
        except TypeError:
            self.__rows_count = 0
            self.__columns_count = 0
        else:
            self.__values = values

    def __str__(self):
        result = ''
        for row in self.__values:
            row = map(str, row)
            for value in row:
                result += f'{value:>4}'
            result += '\n'
        return result

    def __getitem__(self, index: [int, int]):
        """ Get item at index [row][col]. If value doesn't exist return None """
        row, col = index
        try:
            result = self.__values[row][col]
        except IndexError:
            result = None
        return result

    def __add__(self, other):
        """ Addition of the same size matrices.
            If the matrix is not rectangular, nonexistent values are set as default
            If the value being added differs from the original by type the result will be the original value """
        result = []

        # add another matrix if it has the same max size
        if isinstance(other, Matrix) and self.get_size() == other.get_size():
            rows_count, columns_count = self.get_size()

            # Сделал через индексы, чтобы при сложении матриц неправильной формы получалась матрица "правильной" формы
            for row_index in range(rows_count):
                new_row = []
                for col_index in range(columns_count):
                    original_value = self[row_index, col_index]     # get original value
                    adding_value = other[row_index, col_index]      # get adding value
                    new_value = self.__calc_new_value(original_value, adding_value)
                    # adding value to the matrix
                    new_row.append(new_value)
                result.append(new_row)
        else:
            # Return original matrix if another is not Matrix or size differs
            # or raise exception if required
            result = self
        return Matrix(result, self.__default_zero_value)

    def __calc_new_value(self, original_value, adding_value):
        """ Calculating new value """
        # v1
        new_value = original_value + adding_value \
            if isinstance(original_value, type(adding_value)) and original_value and adding_value else \
            original_value if original_value else \
            adding_value if adding_value else \
            self.__default_zero_value

        # v2
        # if isinstance(original_value, type(adding_value)) and original_value and adding_value:
        #     new_value = original_value + adding_value
        # else:
        #     # refresh values switcher
        #     values_switcher = {(True, True): original_value,
        #                        (True, False): original_value,
        #                        (False, True): adding_value,
        #                        (False, False): self.__default_zero_value}
        #     # collect the key and get new value
        #     key = (bool(original_value), bool(adding_value))
        #     new_value = values_switcher.get(key)

        return new_value

    def get_size(self):
        return tuple([self.__rows_count, self.__columns_count])


def task_1():
    print('Task 1 started:')
    data = DataRandom(elem_count=4, nested_elem_count=10, int_bundle=(-20, 20), types=int, nested_level=1)
    mtx1 = Matrix(data.random_list())
    mtx2 = Matrix(data.random_list())
    print(mtx1, '\n', mtx2, sep='')
    mtx = mtx1 + mtx2
    print(mtx)

    # матрица моожет быть неправильной формы и может содержать как числа, так и строки
    mtx1 = Matrix([['a', 'b'], [7, 'e'], ['g', 'h', 'i']], default='-')
    mtx2 = Matrix([['s'], [2, '4', 'f'], ['z']])
    print(mtx1 + mtx2, '\nTask 1 finished.')


# 2 v1
class Clothes:
    """ Base class """
    def __init__(self, model=''):
        self._model = model

    @abstractmethod
    def calc_consumption(self):
        pass


class Coat(Clothes):
    def __init__(self, size: int, model=''):
        super().__init__(model)
        self.__size = size

    @property
    def calc_consumption(self):
        return self.__size / 6.5 + 0.5


class Suit(Clothes):
    def __init__(self, height: int, model=''):
        super().__init__(model)
        self.__height = height

    @property
    def calc_consumption(self):
        return 2 * self.__height + 0.3


def task_2_1():
    print('Task 2 v1 started.')
    item = Suit(172)
    print(item.calc_consumption)
    item = Coat(46)
    print(item.calc_consumption)
    print('Task 2 v1 finished.')


# 2 v2
class AllClothes:
    __varieties = {'coat': ('size', lambda size: size / 6.5 + 0.5),
                   'suit': ('height', lambda height: 2 * height + 0.3)}

    def __init__(self, variety: [__varieties], model='', **params):
        self.__model = model
        self.__variety = variety
        self.__params = params

    @property
    def calc_consumption(self):
        param_name, calc_formula = self.__varieties.get(self.__variety)
        value = calc_formula(self.__params.get(param_name))
        return value


def task_2_2():
    print('Task 2 v2 started.')
    item = AllClothes('suit', height=172)
    print(item.calc_consumption)
    item = AllClothes('coat', size=46)
    print(item.calc_consumption)
    print('Task 2 v2 finished.')


# 3
# гугл сошелся на мнении, что декоратор вне класса проще и понятнее
def same_type(function):
    """ Decorator: check if all values are the same type """
    def wrapper(self, arg):
        if isinstance(self, type(arg)):
            result = function(self, arg)
        else:
            result = None
        return result
    return wrapper


class Cell:
    def __init__(self, parts: int):
        self.parts = parts

    def __str__(self):
        return str(self.parts)

    @same_type
    def __add__(self, other):
        return Cell(self.parts + other.parts)

    @same_type
    def __sub__(self, other):
        sub_parts = self.parts - other.parts
        return Cell(sub_parts) if sub_parts > 0 else None

    @same_type
    def __mul__(self, other):
        return Cell(self.parts * other.parts)

    @same_type
    def __truediv__(self, other):
        return Cell(self.parts // other.parts)

    def make_order(self, parts_in_row):
        """ Get parts in order """
        result = ''
        for part in range(1, self.parts + 1):
            end_of_row = '' if part % parts_in_row else '\n'
            result += ''.join('*' + end_of_row)
        return result


def task_3():
    print('Task 3 started.')
    cell_1 = Cell(12)
    cell_2 = Cell(5)
    print('source:', cell_1, cell_2)
    print('sum:', cell_1 + cell_2)
    print('sub1-2:', cell_1 - cell_2)
    print('sub2-1:', cell_2 - cell_1)
    print('mul:', cell_1 * cell_2)
    print('div:', cell_1 / cell_2)

    print(cell_1.make_order(7), '\n')
    print(cell_2.make_order(7))
    print('Task 3 finished.')


# main
if __name__ == '__main__':
    tasks = {'1': task_1, '2-1': task_2_1, '2-2': task_2_2, '3': task_3}

    running = True
    while running:
        inp = input('> ')
        if inp == 'q':
            running = False
        elif callable(tasks.get(inp)):
            tasks.get(inp)()
