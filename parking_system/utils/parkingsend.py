import json
import os
import telebot
if not os.path.exists(os.path.join(os.getcwd(), 'users.json')):
    with open(os.path.join(os.getcwd(), 'users.json'), 'w') as f:
        m = {}
        json.dump(m, f)
def send_mails(dict_mail):
    user_file = os.path.join(os.getcwd(), 'users.json')
    bot = telebot.TeleBot('6487011985:AAGxPhZuR01zCxE0uLB7JYXaTszkdy2RWpg')
    with open(user_file, 'r') as f:
        m = json.load(f)
    for chat_id, email in m.items():
        if dict_mail == email:
            bot.send_message(chat_id, 'Ворота відкриваються.')