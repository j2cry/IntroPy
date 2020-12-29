# 1
def task_1():
    """ Write inputted data to file """
    inp = input('#> ')
    with open('materials/task_1.txt', 'w', encoding='utf-8') as file:
        while inp:
            file.write(inp + '\n')
            inp = input('#1> ')


# 2
def task_2():
    """ Count the number of lines and words in a line """
    from re import findall
    # можно так
    # file = open('task_2.txt', 'r', encoding='utf-8')
    # lines = file.readlines()
    # file.close()
    # for line in lines:
    #     words_count = len(findall(r'\w+', line))  # words in line: можно сливать в list, если эти данные нужны
    #     print(f'Line {lines.index(line) + 1} contains {words_count} words.')
    # print(f'Total {len(lines)} lines.')

    # но если данных в файле очень много, то наверное лучше так
    lines_count = 0
    with open('materials/task_2.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            lines_count += 1
            words_count = len(findall(r'\w+', line))  # words in line: можно сливать в list, если эти данные нужны
            print(f'Line {lines_count} contains {words_count} words.')
            line = file.readline()
        print(f'Total {lines_count} lines.')


# 3
def task_3(bound=20000):
    """ Get staff salaries from file, print average salary and staff with salary less than bound (default=20000) """
    from statistics import mean, median  # вроде в Numpy есть аналогичный метод
    with open('materials/task_3.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        staff_salaries = {}
        while line:
            name = ' '.join(line.split()[:-1])
            # тут хорошо бы добавить проверку, чтоб не напороться на ValueError, но она мне видится актуальной только
            # в случае создания/редактирования анализируемого файла конечным пользователем вручную
            staff_salaries[name] = float(line.split()[-1])
            line = file.readline()
    average_salary = round(mean(staff_salaries.values()), 2)
    print(f'Average salary equals {average_salary}')
    print(f'Median salary equals {median(staff_salaries.values())}')

    print('Employees with low salary:')
    low_salary = {nm: sal for nm, sal in staff_salaries.items() if sal < bound}
    for nm, sal in low_salary.items():
        print(nm, sal)


# 4
def task_4():
    """ Replace words in lines from file and save to another file """
    from re import compile, sub
    translation = {'One': 'Один', 'Two': 'Два', 'Three': 'Три', 'Four': 'Четыре', 'Five': 'Пять', 'Six': 'Шесть',
                   'Seven': 'Семь', 'Eight': 'Восемь', 'Nine': 'Девять', 'Zero': 'Ноль'}
    pattern = compile('|'.join(translation.keys()))

    with open('materials/task_4.txt', 'r', encoding='utf-8') as file, \
            open('materials/task_4_result.txt', 'w', encoding='utf-8') as new_file:
        line = file.readline()
        while line:
            for found_elem in pattern.findall(line):  # replacing
                line = sub(found_elem, translation.get(found_elem), line)
            new_file.write(line)
            line = file.readline()
    print('Done. Check it out.')


# 5
def task_5():
    """ Calc the sum of integers from file """
    from DataRandom import DataRandom  # опять пригодился :)
    numbers = DataRandom(int_bundle=(-100, 100), elem_count=40, types=int, nested_level=0).random_list()
    with open('materials/task_5.txt', 'w', encoding='utf-8') as file:  # writing
        file.write(' '.join([str(num) for num in numbers]))

    with open('materials/task_5.txt', 'r', encoding='utf-8') as file:  # reading
        # можно чтение из файла и обработку прочитанных данных запилить в одну строку:
        # numbers = [int(elem) for elem in file.readline().split()]
        line = file.readline()
    numbers = [int(elem) for elem in line.split()]
    print(sum(numbers))


# 6
def task_6():
    """ Curriculum analyse """
    import re
    # from re import split findall
    with open('materials/task_6.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        subjects = {}
        while line:
            subj, line = re.split(r':', line)
            hours = [int(elem) for elem in re.findall(r'\d+', line)]
            subjects[subj] = sum(hours)
            line = file.readline()
        print(subjects)


def task_6_gen():  # cheat: совсем неохота заполнять кучи данных вручную
    """ Generate file with curriculum """
    from random import shuffle, randint
    subjects = ['Algebra', 'Art', 'Biology', 'Chemistry', 'Computer science', 'English', 'Foreign language',
                'Geography', 'Geometry', 'Health', 'History', 'Literature', 'Maths', 'Music', 'PE (physical education)',
                'Physics', 'Psychology', 'Social studies']
    shuffle(subjects)

    # как правильнее ловить исключения связанные с чтением/записью файлов?
    # кмк, в моем варианте очень много лишнего кода в блоке try
    try:
        with open('materials/task_6.txt', 'w', encoding='utf-8') as file:
            for subj in subjects:
                lectures = randint(-64, 128)
                seminars = randint(-64, 128)
                labs = randint(-64, 128)

                new_line = f'{subj}:'
                new_line += f' {lectures} lectures' if lectures > 0 else ''
                new_line += f' {seminars} seminars' if seminars > 0 else ''
                new_line += f' {labs} labs' if labs > 0 else ''
                new_line += '\n'
                file.write(new_line)
    except OSError:
        print('Unable to write file!')
        return


# 7
def task_7():
    """ Analyse info about companies """
    from re import findall
    import json

    with open('materials/task_7.txt', 'r', encoding='utf-8') as file:
        companies = {}
        line = file.readline()
        while line:  # parsing and generating source
            # parsing read line
            company_name = findall('\"(.+)\"', line)
            company_name = str(*company_name)
            # business_form = str(*re.findall(r'\"\s(\D+)\s', line))
            earnings, expense = list(map(int, findall(r'\d+', line)))[-2:]

            companies[company_name] = earnings - expense  # save required data

            line = file.readline()

    # analyze info
    # можно так
    # profitable_count = len(list(filter(lambda pr: pr > 0, companies.values())))
    # average_profit = sum([profit for profit in companies.values() if profit > 0]) / profitable_count

    # но так код читабельнее
    profitable = [profit for profit in companies.values() if profit > 0]
    average_profit = sum(profitable) / len(profitable)

    analytics = [companies, {'average_profit': average_profit}]

    # dump to JSON
    with open('materials/task_7.json', 'w', encoding='utf-8') as file:
        json.dump(analytics, file)
    print('Done.')


def task_7_gen(count=15):
    """ Generate info about companies """
    from random import choice, randint
    business_forms = ['ПАО', 'НКО', 'АО', 'ООО', 'ГУП']
    firms_info = [f'"Компания {i + 1}" {choice(business_forms)} {randint(0, 70000)} {randint(0, 70000)}\n'
                  for i in range(count)]
    try:
        with open('materials/task_7.txt', 'w', encoding='utf-8') as file:
            file.writelines(firms_info)
    except OSError:
        print('Unable to write file!')


# main
if __name__ == '__main__':
    running = True
    while running:
        cmd = input('> ')
        if cmd == 'q':
            running = False
            continue

        if cmd == '1':
            task_1()
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
        if cmd == '6gen':
            task_6_gen()
        if cmd == '7':
            task_7()
        if cmd == '7gen':
            task_7_gen()
