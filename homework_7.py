

# 1
class Matrix:
    def __init__(self, values: list[list], default=None):
        """ Initialize matrix with values (list of lists) """
        self.__default_zero_value = default
        self.__values = [[]]
        try:
            self.__rows_count = len(values)     # количество строк
            self.__columns_count = max(map(len, values))       # количество столбцов
        except TypeError:
            self.__values = [[]]
            self.__rows_count = 0
            self.__columns_count = 0
        else:
            self.__values = values

    def __str__(self):
        result = ''
        for row in self.__values:
            result += ' '.join(row) + '\n'
        return result

    def __add__(self, other):
        """ Addition of the same size matrices.
            If the matrix is not rectangular, nonexistent values are set as default """
        # calculating size of other matrix
        try:
            rows_count = len(other)
            columns_count = max(map(len, other))
        except TypeError:
            rows_count = 0
            columns_count = 0

        if self.get_size() == (rows_count, columns_count):     # add other matrix if it has the same max size
            for row in range(rows_count):
                for col in range(columns_count):
                    # get old value
                    try:
                        old_val = self.__values[row][col]
                    except IndexError:
                        old_val = None

                    # get other value
                    try:
                        add_val = other[row][col]
                    except IndexError:
                        add_val = None

                    # calculating new value
                    new_val = old_val + add_val if (old_val and add_val and isinstance(old_val, type(add_val))) else \
                        old_val if old_val and not add_val else \
                        add_val if add_val and not old_val else self.__default_zero_value

                    # adding value to the matrix
                    try:
                        self.__values[row][col] = new_val
                    except IndexError:
                        self.__values[row].append(new_val)
        else:
            # raise exception if you want
            pass
        return self

    def get_size(self):
        return tuple([self.__rows_count, self.__columns_count])


# TODO: запилить тестирование Pytest
mtx = Matrix([['a', 'b'], ['d', 'e'], ['g', 'h', 'i']], default='-')
# mtx = Matrix([['a'], ['d'], ['g']], default='-')
# mtx += [['s'], ['q', '0', 'j'], ['z']]
mtx += [['s'], ['2', '4', 'f'], ['z']]
print(mtx)
