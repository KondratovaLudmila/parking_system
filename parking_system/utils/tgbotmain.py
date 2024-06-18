import json
import os
import re

import telebot

bot = telebot.TeleBot('6487011985:AAGxPhZuR01zCxE0uLB7JYXaTszkdy2RWpg')

email_regex = re.compile(
    r"^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?:(?=\S)(?!.*?[ \t])(?:(?<=.)|[^@\s])[a-zA-Z0-9!#$%&'*+/=?^_`{|}~\-]+(?<=\S)(?=\S)@(?=\S)(?=.{1,255})(?:[a-zA-Z0-9](?:(?<!\.)[\-]*[a-zA-Z0-9])*\.)+[a-zA-Z]{2,63}(?<=\S))$"
)

if not os.path.exists(os.path.join(os.getcwd(), 'users.json')):
    with open(os.path.join(os.getcwd(), 'users.json'), 'w') as f:
        m = {}
        json.dump(m, f)

user_file = os.path.join(os.getcwd(), 'users.json')


def is_valid_email(email):
    if re.match(email_regex, email):
        return True
    return False


def check_user(chat_id):
    with open(user_file, 'r') as f:
        m = json.load(f)
    if str(chat_id) in set(m):
        return True
    return False


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, 'Вітаю вас! Введіть email для підтвердження акаунту.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_activate(message):
    if message.chat.type == 'private':
        if not check_user(message.chat.id):
            if is_valid_email(message.text):
                with open(user_file, 'r') as f:
                    m = json.load(f)
                m[str(message.chat.id)] = message.text
                with open(user_file, 'w') as f:
                    json.dump(m, f)

                bot.send_message(message.chat.id, 'Вас підтверджено.')
            else:
                bot.send_message(message.chat.id, 'Некоректно введений email.')


bot.polling(none_stop=True)
