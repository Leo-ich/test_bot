#!/usr/bin/env python3

from os import environ

from flask import Flask, request
from config import Config

from telebot import types
from tg_bot import bot

app = Flask(__name__)
app.config.from_object(Config)

TOKEN = app.config.get('API_TOKEN') or environ['API_TOKEN']


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    host = app.config.get('WEBHOOK_HOST', '')
    if host:
        bot.set_webhook(url=host + TOKEN)
    return "!", 200


if __name__ == '__main__':
    app.run(host=app.config['WEBHOOK_LISTEN'],
            port=app.config['WEBHOOK_PORT'])
