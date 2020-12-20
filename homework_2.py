# 1
def task_1():
    data = ['qwerty', 0xF0, 3.14, ['v1', None, 7.62], {0: "value", "key": 17}, None]
    for d in data:
        print(type(d).__name__)


# 2
def task_2():
    data = input('Enter values (space as delimiter): ').split()
    for i in range(0, (len(data) // 2) * 2, 2):
        data[i], data[i + 1] = data[i + 1], data[i]
    print(data)


# 3
def task_3():
    seasons = {'winter': [12, 1, 2], 'spring': [3, 4, 5], 'summer': [6, 7, 8], 'autumn': [9, 10, 11]}
    month = int(input('Enter a month (1-12): '))
    if 0 < month < 13:
        for season, months in seasons.items():
            if month in months:
                print(season)
    else:
        print('Invalid month!')


# 4
def task_4():
    src_string = input('Enter some values (space as delimiter): ').split()
    for s in enumerate(src_string, 1):
        print(f'{s[0]}: {s[1][:10]}')


# 5
def task_5():
    running = True
    rates = []
    while running:
        command = input("Enter rate (or 'exit'): ")
        if command == 'exit':
            running = False
            continue
        try:
            new_rate = int(command)
        except ValueError:
            print('Invalid rate! Try again.')
            continue

        # это решение при простой структуре данных дает нужный результат, но при вложенных структурах требует усложнения
        # фильтров сортировки, иначе условие "при равных значениях рейтинга вставлять в конец" может не соблюдаться
        # rates.append(new_rate)
        # rates.sort(reverse=True)

        # insert element: elem_a >= new_rate > elem_b
        for i, rate in enumerate(rates):
            if rate < new_rate:
                rates.insert(i, new_rate)
                break
        else:   # for cases: (1) new_rate is the first element; (2) new_rate is minimal element
            rates.append(new_rate)
        print(rates)


# 6*
def task_6():
    from operator import itemgetter

    # Step 1. Collecting data
    input_format = '[number] [name] [price] [quantity] [unit]'
    # if the number should not be requested from the user
    # input_format = '[name] [price] [quantity] [unit]'
    print(f"Input format: {input_format}")
    data_collecting = True
    goods = []

    while data_collecting:
        # data input
        new_input = input("Enter product info (or 'exit'): ")
        if new_input == 'exit':
            data_collecting = False
            continue

        # Безопасно ли такое обращение? или лучше брать со среза? new_input = new_input[:].split()
        new_input = new_input.split()  # NOTE: ?change the separator for ability to use spaces in the name?
        # analyze input
        try:
            new_product = (int(new_input[0]), {'name': new_input[1], 'price': float(new_input[2]),
                                               'quantity': float(new_input[3]), 'unit': new_input[4]})
            # if the number should not be requested from the user:
            # new_product = {'name': new_input[0], 'price': float(new_input[1]), 'quantity': float(new_input[2]),
            #                'unit': new_input[3]}

        except ValueError:  # price and/or quantity is not numeric
            print('Invalid input format! Number, price and quantity must be numeric.')
            # if the number should not be requested from the user:
            # print('Invalid input format! Price and quantity must be numeric.')
            continue
        except IndexError:  # the number of specified parameters is less than necessary
            print(f'Invalid input format! Format: {input_format}')
            continue
        else:
            goods.append(new_product)

    # if the number should not be requested from the user, generating the necessary data structure:
    # goods = list(enumerate(goods, 1))

    # Step 2. Analyzing data (matching keys in dicts is not required)
    # collect unique keys from all dicts
    keys = {key for num, product in goods for key in product.keys()}

    # data conversion

    # goods_analytics = dict()
    # for key in keys:
    #     values = []
    #     for num, product in goods:
    #         values.append(product.get(key))
    #         goods_analytics[key] = values
    # print(goods_analytics)

    # products = [product for num, product in goods]
    goods_analytics = {key: list(map(itemgetter(key), [product for num, product in goods])) for key in keys}
    print(goods_analytics)


if __name__ == "__main__":
    cmd = input('Enter task number: ')

    if cmd == '1':
        task_1()
    elif cmd == '2':
        task_2()
    elif cmd == '3':
        task_3()
    elif cmd == '4':
        task_4()
    elif cmd == '5':
        task_5()
    elif cmd == '6':
        task_6()
    else:
        print('Incorrect input!')
