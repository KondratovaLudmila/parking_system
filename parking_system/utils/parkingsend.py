import json
import os
import telebot
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

WORK_DIR = Path(__file__).parent.parent.resolve()
USERS_JSON = WORK_DIR.joinpath('bot_files', 'users.json')

if not USERS_JSON.exists():
    USERS_JSON.parent.mkdir(parents=True)
    try:
        with open(USERS_JSON, 'w') as f:
            m = {}
            json.dump(m, f)
    
    except Exception as err:
        print(err)


def tg_notify(dict_mail):
    bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'))
    try:
        with open(USERS_JSON, 'r') as f:
            m = json.load(f)
    
    except Exception as err:
        print(err)
        m = {}

    chat_id = m.get(dict_mail)
    if chat_id:
        bot.send_message(chat_id, 'Ворота відкриваються.')