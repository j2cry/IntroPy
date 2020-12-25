from DataRandom import DataRandom


# 1
def task_1():     # using argparse - сделал просто ради посмотреть, как это работает.
    """Salary calculation (using terminal)"""
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-wh', type=float, dest='working_hours', required=True)
    parser.add_argument('-rt', type=float, dest='rate_per_hour', required=True)
    parser.add_argument('-bs', type=float, dest='bonus', required=True)
    args = parser.parse_args()
    print('Salary = ', round(args.working_hours * args.rate_per_hour + args.bonus, 2))


def task_1_1():
    import sys
    if len(sys.argv) < 3:
        print('Not enough arguments!')
        return
    try:
        working_hours = float(sys.argv[1])
        rate_per_hour = float(sys.argv[2])
        bonus = float(sys.argv[3])
    except ValueError:
        print('All arguments must be numeric!')
        return
    print('Salary = ', round(working_hours * rate_per_hour + bonus, 2))


# 2
def next_element(iterable):
    if iterable:
        iterator = iter(iterable)
        current_elem = next(iterator)
        for next_elem in iterator:
            yield current_elem, next_elem
            current_elem = next_elem


def task_2():
    """Elements that meet the condition: current element > previous element """
    source = [300, 2, 12, 44, 1, 1, 4, 10, 7, 1, 78, 123, 55]
    modified = [nxt for cur, nxt in next_element(source) if nxt and nxt > cur]
    print(source)
    print(modified)

    # checking with random data
    data = DataRandom(int_bundle=(0, 100), elem_count=20, types=int, nested_level=0)
    source = data.random_list()
    modified = [nxt for cur, nxt in next_element(source) if nxt and nxt > cur]
    print(source)
    print(modified)


# 3
def task_3():
    """Print numbers in [20, 240] that are multiples of 20 and 21. One-string solution"""
    print([num for num in range(20, 240) if not num % 20 or not num % 21])


# 4
def task_4():    # можно еще через collections.Counter(), но кода получится ощутимо больше
    """Get non-repeating elements from list"""
    source = [2, 2, 2, 7, 23, 1, 44, 44, 3, 2, 10, 7, 4, 11]
    modified = [elem for elem in source if source.count(elem) == 1]
    print(source)
    print(modified)

    # checking with random data
    data = DataRandom(int_bundle=(0, 50), elem_count=20, types=int, nested_level=0)
    source = data.random_list()
    modified = [elem for elem in source if source.count(elem) == 1]
    print(source)
    print(modified)


# 5
def task_5():
    """Product of all elements in range"""
    from functools import reduce
    source = [num for num in range(100, 1001, 2)]
    print(f'{reduce(lambda a, b: a*b, source)}')


# 6
def task_6():       # честно, не очень понял смысл задачи
    """count() and cycle() usage"""
    from itertools import count
    from itertools import cycle

    print('count() example:')
    for num in count(12):
        if num > 23:
            print('STOPPED')
            break
        print(num, end='->')

    print('cycle() example:')
    st = ['german', 'shepherds', 'are', 'the', 'best', 'dogs', '!']
    cnt = 0
    for s in cycle(st):
        print(s, end=' ')
        cnt += 1
        if cnt == 17:
            print('THE BEST!!!')
            break


# 7
def task_7_factorial(end=4):
    result = 1
    for num in range(1, end + 1):
        result *= num
        yield result


def task_7():
    for fact in task_7_factorial(10):
        print(fact)


# main
if __name__ == '__main__':
    running = True
    while running:
        cmd = input('> ')
        if cmd == 'exit':
            running = False
            continue

        if cmd == '1':
            task_1()
        if cmd == '1-1':
            task_1_1()
        if cmd == '2':
            task_2()
        if cmd == '3':
            task_3()
        if cmd == '4':
            task_4()
        if cmd == '5':
            task_5()
        if cmd == '6':
            task_6()
        if cmd == '7':
            task_7()
