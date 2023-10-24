import telebot
from secret import TOKEN
from telebot import types

import random

bot = telebot.TeleBot(TOKEN)

story = ["Мужик возвращается домой под утро пьяный.\
        Открывает дверь, при этом задевает стремянку,\
        та рушится на велосипед, он сшибает на пол вазу, ваза падает на кота… Из комнат выглядывают жена и сын.\
        Что, не спится без папки?",
         "петька петрович",
         ]
name = ''
surname = ''
age = 0



@bot.message_handler(content_types=['text'])
def start(message):
    global story
    bot.send_message(message.from_user.id, 'Напиши /joke')
    if message.text == '/joke':
        bot.send_message(message.from_user.id, random.choice(story))
    else:
        bot.send_message(message.from_user.id, 'Напиши /joke')


bot.polling(none_stop=True, interval=0)