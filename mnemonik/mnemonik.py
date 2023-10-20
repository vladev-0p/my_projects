import random
import os
import time
from time import time
from threading import Timer
from inputimeout import inputimeout

words = ['положение',
         'трубка',
         'присутствие',
         'соединение',
         'начальник',
         'рубеж',
         'произведение',
         'поселок',
         'минута',
         'безопасность',
         'прошлое',
         'ответ',
         'слой',
         'лошадь',
         'девушка',
         'врач',
         'роман',
         'февраль', 'автомобиль',
         'депутат',
         'малина',
         'кошка',
         'собака',
         ]

m = int(input('Выберите число слов - '))


def timer_word(n):
    time.sleep(n*2.5)
    print('\n' * 10)


num = 0


while True:
    random_list = random.sample(words, m)
    for i in random_list:
        print(i, end=' ', flush=True)
    timer_word(m)
    answer = [input('Введите слова: ') for i in range(m)]
    if answer == random_list and m < 8:
        print('верно')
        num += 1
    if num == 2:
        m += 1
        num = 0


