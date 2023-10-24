import random
import os
import time
from threading import Timer
from inputimeout import inputimeout

words = ['condition',
         'pipe',
         'presence',
         'connection',
         'chief',
         'border',
         'произведение',
         'village',
         'minute',
         'safety',
         'past',
         'answer',
         'layer',
         'horse',
         'lady',
         'doctor',
         'roman',
         'february', 'car',
         'deputy',
         'raspberry',
         'cat',
         'dog',
         ]

m = int(input('Choose words amount - '))


def timer_word(n):
    time.sleep(n*2.5)
    print('\n' * 10)


num = 0


while True:
    random_list = random.sample(words, m)
    for i in random_list:
        print(i, end=' ', flush=True)
    timer_word(m)
    answer = [input('Enter words: ') for i in range(m)]
    if answer == random_list and m < 8:
        print('Correct')
        num += 1
    if num == 2:
        m += 1
        num = 0


