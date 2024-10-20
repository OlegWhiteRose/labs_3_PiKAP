import json
import sys
# Сделаем другие необходимые импорты
from field import field
from unique import Unique
from print_result import print_result
from cm_timer import *
from gen_random import gen_random

path = 'data/data_light.json'

# Необходимо в переменную path сохранить путь к файлу, который был передан при запуске сценария

with open(path) as f:
    data = json.load(f)

# Далее необходимо реализовать все функции по заданию, заменив `raise NotImplemented`
# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(arg):
    return sorted(Unique([list(x.values())[0] for x in field(arg, 'job-name')], ignore_case = True), key=lambda x: (x.lower(), x)) 


def filter(arg):
    for s in arg:
        if s.strip().lower().startswith('программист'):
            yield s


@print_result
def f2(arg):
    return [x for x in filter(arg)]


@print_result
def f3(arg):
    return list(map(lambda x: f'{x} с опытом Python', arg))


@print_result
def f4(arg):
    salaries = gen_random(len(arg), 100_000, 200_000)
    return [f'{x[0]}, зарплата {x[1]} руб' for x in zip(arg, salaries)]


if __name__ == '__main__':
    with cm_timer_2():
        f4(f3(f2(f1(data))))