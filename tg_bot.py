#!/usr/bin/env python3

from os import environ
import logging
import datetime

from telebot import TeleBot, logger

from config import Config

logger.setLevel(logging.INFO)

TOKEN = getattr(Config, 'API_TOKEN', '') or environ['API_TOKEN']
bot = TeleBot(TOKEN)

# TODO save in file
knownUsers = []
userStep = {}

commands = {  # command description used in the "help" command
    'start': 'Начать использование бота',
    'help': 'Информация о всех доступных командах',
    'new': 'Начать оформление новой автостраховки',
}


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print('Обнаружен новый пользователь, который не использовал \"/start\"')
        return 0


@bot.message_handler(commands=['start'])
def cmd_start(msg):
    chat_id = msg.chat.id
    if chat_id not in knownUsers:
        knownUsers.append(chat_id)
        userStep[chat_id] = 0
        command_help(msg)
        command_new(msg)
    else:
        print('Уже известный пользователь %s, использовал \"/start\"'
              % msg.from_user.first_name)
        command_help(msg)
        command_new(msg)


@bot.message_handler(commands=['help'])
def command_help(msg):
    chat_id = msg.chat.id
    help_text = 'Этот бот симулирует оформление автостраховки. ' \
                'Доступны следующие команды: \n'
    for key in commands:
        help_text += '/' + key + ': '
        help_text += commands[key] + '\n'
    bot.send_message(chat_id, help_text)


@bot.message_handler(commands=['new'])
@bot.message_handler(func=lambda msg: get_user_step(msg.chat.id) == 0,
                     content_types=['text'])
def command_new(msg):
    chat_id = msg.chat.id
    userStep[chat_id] = 1
    bot.send_message(chat_id, 'Ваше имя?')


@bot.message_handler(func=lambda msg: get_user_step(msg.chat.id) == 1,
                     content_types=['text'])
def get_username(msg):
    chat_id = msg.chat.id
    print(msg.text)
    if len(msg.text) >= 255:
        bot.send_message(chat_id, 'Имя должно быть короче 255 букв')
        return
    userStep[chat_id] = 2
    bot.send_message(chat_id, 'Ваша фамилия?')


@bot.message_handler(func=lambda msg: get_user_step(msg.chat.id) == 2,
                     content_types=['text'])
def get_last_name(msg):
    chat_id = msg.chat.id
    print(msg.text)
    if len(msg.text) >= 255:
        bot.send_message(chat_id, 'Фамилия должна быть короче 255 букв')
        return
    userStep[chat_id] = 3
    bot.send_message(chat_id, 'Марка вашего автомобиля?')


@bot.message_handler(func=lambda msg: get_user_step(msg.chat.id) == 3,
                     content_types=['text'])
def get_car_model(msg):
    chat_id = msg.chat.id
    print(msg.text)
    if len(msg.text) >= 255:
        bot.send_message(chat_id, 'Марка авто должна быть короче 255 букв')
        return
    userStep[chat_id] = 4
    bot.send_message(chat_id, 'Год выпуска вашего автомобиля?')


@bot.message_handler(func=lambda msg: get_user_step(msg.chat.id) == 4,
                     content_types=['text'])
def get_car_year(msg):
    chat_id = msg.chat.id
    print(msg.text)
    cur_year = datetime.datetime.now().year
    err_text = 'Год должен быть числом между 1970 и %s.' \
               ' Попробуйте ещё раз' % cur_year
    if not msg.text.isdigit():
        bot.send_message(chat_id, err_text)
        return
    if not (1970 <= int(msg.text) <= int(str(cur_year))):
        bot.send_message(chat_id, err_text)
        return
    userStep[chat_id] = 5
    bot.send_message(chat_id, 'Мощность вашего автомобиля?')


@bot.message_handler(func=lambda msg: get_user_step(msg.chat.id) == 5,
                     content_types=['text'])
def get_car_power(msg):
    chat_id = msg.chat.id
    print(msg.text)
    err_text = 'Мощность должна быть числом между 0 и 2000.'
    if not msg.text.isdigit():
        bot.send_message(chat_id, err_text)
        return
    if not (0 < int(msg.text) <= 2000):
        bot.send_message(chat_id, err_text)
        return
    userStep[chat_id] = 6
    bot.send_message(chat_id, 'Спасибо за ответы, вам оформлен'
                              ' полис номер ХХХ. \n/help')


@bot.message_handler(func=lambda msg: True, content_types=['text'])
def echo_message(msg):
    chat_id = msg.chat.id
    userStep[chat_id] = 0
    bot.send_message(chat_id, 'Сбой бота, жду новой команды')
    command_help(msg)


if __name__ == '__main__':
    bot.polling()
