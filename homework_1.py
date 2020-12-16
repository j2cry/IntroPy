# 1
def task_1():
    num = input('Enter a number: ')
    if num.isdigit():
        print(f'If this number is divided by 10, you get {int(num) / 10}')

    color = input('Enter a color: ')
    fruit = input('Enter a fruit: ')
    print(f'Do you have a {color} {fruit}?!')


# 2
def task_2():
    sec = int(input('Enter the time (in seconds): '))
    hh = sec // 3600
    mm = (sec - hh * 3600) // 60
    ss = (sec - hh * 3600 - mm * 60)
    print(f'{hh}:{mm}:{ss}')


# 3
def task_3():
    n = input('Enter a number: ')
    res = int(n) + int(n * 2) + int(n * 3)
    print(res)


# 4
def task_4():
    num = int(input('Enter a positive integer: '))
    n = num
    if num > 0:
        # отсекаем сзади первую цифру и принимаем ее за наибольшую
        mx = num % 10
        num = num // 10
        # пока в числе есть цифры
        while num > 0:
            # отсекаем сзади по одной цифре
            next_n = num % 10
            # и находим наибольшую
            mid = (next_n + mx) / 2
            mx = int(mid + abs(next_n - mx) / 2)
            # вот вариант компактнее, но меньше арифметики:
            # if num % 10 > mx:
            #     mx = num % 10
            num = num // 10
        print(f'Max digit in number {n} is {mx}')

        # Или вообще можно так, но это не соответствует условию задачи:
        # max = max(list(str(num)))
    else:
        print('You entered a negative integer!')


# 5
def task_5():
    earnings = int(input('Enter earnings: '))
    expenses = int(input('Enter expenses: '))

    profit = earnings - expenses
    if profit > 0:
        rate = round(profit / earnings, 4)
        print(f'Things are goin\' well! Profitability = {rate}')
        staff = int(input('Enter number of staff: '))
        print(f'Profit per employee is {round(profit / staff, 4)}')
    else:
        print("Unfortunately, it's not going very well.")


# 6
def task_6():
    a = int(input('Enter the result on the first day: '))
    b = int(input('Enter the final result: '))

    i = 1
    res = a
    while res < b:
        # print(f'day {i}: {round(res, 2)}')
        i += 1
        res *= 1.1

    print(f'The result will be achieved on day {i}')
