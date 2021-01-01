from itertools import cycle
from sched import scheduler
from threading import Thread
from time import sleep
from random import randint


# 1 v1
class TrafficLightThread:
    def __init__(self, iterations=6):
        self.__states = {'red': 7, 'yellow': 2, 'green': 5}
        self.__color = ''
        self.__running = False
        self.__light_changer = Thread(target=self.__change_color)

    def run(self):
        """ Turn on the traffic light """
        self.__running = True
        self.__light_changer.start()

    def stop(self):
        """ Turn off the traffic light """
        self.__running = False

    @property
    def running(self):
        """ Get traffic light running status """
        return self.__running

    def __change_color(self):
        """ Set traffic light to the next state """
        print('Traffic light is turned up in loop mode.')
        states_generator = self.__get_next_color()
        while self.__running:
            # get next state
            self.__color = next(states_generator)
            print(f'Traffic light color: {self.__color}')
            sleep(self.__states.get(self.__color))
        print('Traffic light is turned down.')

    def __get_next_color(self):
        """ Get next state of traffic light """
        for state in cycle(self.__states):
            yield state
        else:
            return


def task_1_1():
    """ Test for task 1 v1 """
    if not light_1.running:
        light_1.run()
    else:
        light_1.stop()


# 1 v2
class TrafficLightScheduler:
    def __init__(self, iterations=6):
        self.__states = {'red': 7, 'yellow': 2, 'green': 5}
        self.__color = ''
        self.__states_generator = self.__get_next_color()
        self.__iterations = iterations
        self.__light_changer = scheduler()
        self.__next_state_event = self.__light_changer.enter(0, 1, self.__change_state, ())

    def run(self):
        """ Turn on the traffic light """
        print(f'Traffic light is turned up.')
        self.__light_changer.run()

    def stop(self):
        """ Turn off the traffic light """
        self.__color = ''
        if not self.__light_changer.empty():
            self.__light_changer.cancel(self.__next_state_event)
        print('Traffic light is turned down.')

    def __change_state(self):
        """ Set traffic light to the next state """
        # generating next state
        try:
            self.__color = next(self.__states_generator)
        except StopIteration:
            self.stop()
            return
        print(f'Traffic light color: {self.__color}')
        # set scheduler
        self.__next_state_event = self.__light_changer.enter(self.__states.get(self.__color), 1, self.__change_state, ())

    def __get_next_color(self):
        """ Get next state of traffic light """
        cnt = 0
        for state in cycle(self.__states):
            if cnt < self.__iterations:
                yield state
                cnt += 1
            else:
                return


def task_1_2():
    """ Test for task 1 v2 """
    light_2 = TrafficLightScheduler()
    light_2.run()


# 2
class Road:
    def __init__(self, length, width):
        self._length = length
        self._width = width

    def mass_count(self, height, mass_per_square=25):
        """ Count mass of asphalt, required for the all road
            mass_per_unit: mass of asphalt, required for 1x1x0.01 m of the road"""
        return self._length * self._width * mass_per_square * height


def task_2():
    """ Test for task 2 """
    road = Road(5000, 20)
    print(road.mass_count(5), 'kg')


# 3
class Worker:
    def __init__(self, name, surname, position, wage, bonus):
        self.name = name
        self.surname = surname 
        self.position = position
        self._income = {'wage': wage, 'bonus': bonus}


class Position(Worker):
    def get_full_name(self):
        return self.name, self.surname

    def get_total_income(self):
        return sum(self._income.values())


def task_3():
    """ Test for task 3 """
    worker = Position('Adam', 'Jensen', 'Chief of Security', 8320, 4750)
    print('Full name:', *worker.get_full_name(), 'Total income:', worker.get_total_income())


#4
class Car:
    def __init__(self, name, color, speed, is_police):
        self._speed = speed
        self._color = color
        self._name = name
        self._is_police = is_police
        self._direction = 0

    def go(self, speed=5):
        """ Start driving """
        self._speed = abs(speed) if speed else self._speed

    def stop(self):
        """ Stop driving """
        self._speed = 0

    def turn(self, direction):
        """ Turn to direction """
        self._direction = direction

    def show_speed(self):
        return f'Your speed is {self._speed}. '

    def status(self) -> str:
        """ Get actual parameters """
        return f'{self._name} ({self._color}). {self.show_speed()}Direction is {self._direction}. ' \
               f'It is {"" if self._is_police else "not "}a police car.'
    # @property
    # def speed(self):
    #     return self.speed
    #
    # @speed.setter
    # def speed(self, speed):
    #     self.speed = speed


class TownCar(Car):
    def __init__(self, name, color, speed, is_police):
        super().__init__(name, color, speed, is_police)
        self._max_speed = 60

    def show_speed(self):
        return f'Your speed is {self._speed}. {"You are over-speeding. " if self._speed > self._max_speed else ""}'


class WorkCar(TownCar):
    def __init__(self, name, color, speed, is_police):
        super().__init__(name, color, speed, is_police)
        self._max_speed = 40


class SportCar(Car):    # а тут не сказано ничего менять :(
    pass


class PoliceCar(Car):
    def __init__(self, name, color, speed):
        super().__init__(name, color, speed, is_police=True)


def task_4():
    """ Test for task 4 """
    cars = [Car('Car', 'red', 0, False),
            TownCar('Town car', 'blue', 0, False),
            WorkCar('Taxi', 'yellow', 150, False),
            PoliceCar('Police car', 'white', 0)]

    for car in cars:
        print(car.status())
        for spd in range(30, 71, 20):
            car.go(spd)
            car.turn(randint(0, 361))
            print(car.status())
        print('')


# 5
class Stationery:
    def __init__(self):
        self._title = ''

    def draw(self):
        return 'Start drawing.'


class Pen(Stationery):
    def draw(self):
        return 'Drawing with pen.'


class Pencil(Stationery):
    def draw(self):
        return 'Drawing with pencil.'


class Handle(Stationery):
    def draw(self):
        return 'Drawing with handle.'


def task_5():
    """ Test for task 5 """
    office_supplies = [Stationery(), Pen(), Pencil(), Handle()]
    for supply in office_supplies:
        print(supply.draw())


# main
if __name__ == '__main__':
    running = True
    # кажется, я начал понимать, как это работает
    tasks = {'1-1': task_1_1, '1-2': task_1_2, '2': task_2, '3': task_3, '4': task_4, '5': task_5}
    light_1 = TrafficLightThread()

    while running:
        cmd = input('> ')

        if cmd in tasks.keys() and callable(tasks.get(cmd)):
            tasks.get(cmd)()
        elif cmd == 'q':
            running = False
            # continue  # вернуть, если добавится что-либо после блока if
