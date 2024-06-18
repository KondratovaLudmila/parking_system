import json
import os
import re

import telebot
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

WORK_DIR = Path(__file__).parent.parent.resolve()
USERS_JSON = WORK_DIR.joinpath('bot_files', 'users.json')

bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'))

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email_pattern2 = r"^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?:(?=\S)(?!.*?[ \t])(?:(?<=.)|[^@\s])[a-zA-Z0-9!#$%&'*+/=?^_`{|}~\-]+(?<=\S)(?=\S)@(?=\S)(?=.{1,255})(?:[a-zA-Z0-9](?:(?<!\.)[\-]*[a-zA-Z0-9])*\.)+[a-zA-Z]{2,63}(?<=\S))$"

email_regex = re.compile(email_pattern)

if not USERS_JSON.exists():
    try:
        USERS_JSON.parent.mkdir(parents=True)
        with open(USERS_JSON, 'w') as f:
            m = {}
            json.dump(m, f)
    except Exception as err:
        print(err)


def is_valid_email(email):
    if re.match(email_regex, email):
        return True
    return False


def check_user(email: str):
    try:
        with open(USERS_JSON, 'r') as f:
            m = json.load(f)
    except Exception as err:
        print(err)
        m = {}

    if email in m:
        return True
    return False


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, 'Вітаю вас! Введіть email для підтвердження акаунту.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_activate(message):
    if message.chat.type == 'private':
        if not is_valid_email(message.text):
            bot.send_message(message.chat.id, 'Некоректно введений email.')
        
        if not check_user(message.text):
            with open(USERS_JSON, 'r') as f:
                m = json.load(f)
            
            m[message.text] = message.chat.id
            with open(USERS_JSON, 'w') as f:
                json.dump(m, f)

            bot.send_message(message.chat.id, 'Вас підтверджено.')


bot.polling(none_stop=True)
