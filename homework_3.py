# 1
def task_1(a, b):
    """Division of numbers with verification"""
    try:
        res = float(a) / float(b)
    except ZeroDivisionError:
        return 'Division by zero!'
    except ValueError:
        return 'Not numeric arguments!'
    else:
        return f'a / b = {round(res, 4)}'


# 2
def task_2(first_name="", last_name="", birth_year="", city="", mail="", phone=""):
    """Func with named args and single-line output"""
    return f'first name: {first_name}; last name: {last_name}; year of birth: {birth_year}; city: {city}; ' \
        f'e-mail: {mail}; phone: {phone}'


# 3 my_func()
def task_3(a, b, c):
    """Finding the sum of the two largest arguments out of three"""
    return sum([a, b, c]) - min(a, b, c)    # просто, понятно, компактно, но не работает для строк

    # если прям надо знать эти аргументы + работает для строк
    # mx1 = max(a, b)
    # mx2 = max(b, c) if mx1 != max(b, c) else max(a, c)
    # return mx1 + mx2

    # ну или опять же сортировка
    # lst = sorted([a, b, c], reverse=True)
    # return sum(lst[:2])     # lst[0] + lst[1] если надо, чтоб работало и со строками тоже


# 4 v1
def task_4_1(x, y):
    """Raising to an integer negative power"""
    if y >= 0 or x <= 0:
        return None

    # return x ** y     # самый простой способ
    res = x
    for i in range(abs(y) - 1):
        res *= x
    return 1 / res


# 4 v2
def task_4_2(x, y) -> 'x ** y':
    if y > 0 or x <= 0:
        return None
    if y == -1:
        return 1 / x
    return task_4_2(x, y + 1) / x


# 5 v1
def task_5_1():
    """Calculating the sum of inputted numbers and exit by special character"""
    running = True
    # num_list = []     # if it is required to save values
    amount = 0
    while running:
        inp = input('Enter some numbers (enter "#" to exit): ').split()
        for elem in inp:
            if elem == "#":
                running = False
                break   # comment if it is required to add numbers after the spec char
            try:
                amount += float(elem)
                # num_list.append(float(elem))    # if it is required to save values
            except ValueError:
                continue    # skip non-numeric input
        # print(f'Amount of {num_list} = {sum(num_list)}')   # if it is required to save values
        print(f'Amount = {amount}')


# 5 v2
def task_5_iter(iterable):
    iterator = iter(iterable)
    for elem in iterator:
        try:
            yield float(elem)
        except ValueError:
            # pass
            if elem == '#':     # pass if it is required to add numbers after the spec char
                return


def task_5_2():
    inp = ''
    amount = 0
    while '#' not in inp:
        inp = input('Enter some numbers (enter "#" to exit): ').split()
        nums = [elem for elem in task_5_iter(inp)]
        amount += sum(nums)
        print(f'Amount = {amount}')


# 6
def task_6():
    words = input('Enter some words: ')
    print(int_func(words))


def int_func(word):
    return word.title()     # или можно capitalize() с итерацией for word in words


# main
if __name__ == '__main__':
    running = True
    while running:
        cmd = input('> ')
        if cmd == 'exit':
            running = False
            continue

        if cmd == '1':
            inp = input('Enter two integers: ').split()
            if len(inp) >= 2:
                print(task_1(inp[0], inp[1]))
            else:
                print('Not enough arguments!')
        elif cmd == '2':
            user = {'first_name': 'Adriano', 'last_name': 'Celentano', 'birth_year': 1938, 'city': 'Milano'}
            print(task_2(**user, phone='not available', mail='not available'))

        elif cmd == '3':
            a, b, c = 3, 11, 7
            print(a, b, c, '-->', task_3(a, b, c))
            print(a, c, b, '-->', task_3(a, c, b))
            print(b, a, c, '-->', task_3(b, a, c))
            print(b, b, a, '-->', task_3(b, b, a))
            print(b, a, b, '-->', task_3(b, a, b))
            # print(my_func('DD', 'W', 'G'))
        elif cmd == '4-1':
            a, b = 7, -5
            print(f'{a}^{b} = {task_4_1(a, b):g}')
            a, b = 0.7, -6
            print(f'{a}^{b} = {task_4_1(a, b):g}')
        elif cmd == '4-2':
            a, b = 7, -5
            print(f'{a}^{b} = {task_4_2(a, b):g}')
            a, b = 0.7, -6
            print(f'{a}^{b} = {task_4_2(a, b):g}')
        elif cmd == '5-1':
            task_5_1()
        elif cmd == '5-2':
            task_5_2()
        elif cmd == '6':
            task_6()
