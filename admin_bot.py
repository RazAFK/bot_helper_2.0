import telebot, time, pprint, jsonpickle, json
from settings.TOKEN import *
from db import *


abot = telebot.TeleBot(admin_token)



@abot.message_handler(commands=['stop']) 
def stop(message):
    if message.chat.id == 1634714523:
        abot.send_message(message.chat.id, 'Остановка')
        abot.stop_bot()
        exit()
    else:
        abot.send_message(message.chat.id, 'Недостаточно полномочий')


@abot.message_handler(commands=['start'])
def start(message):
    abot.send_message(message.chat.id, 'Hey')
    pprint.pprint(vars(message))





if __name__ == "__main__":
    try:
        abot.polling(none_stop=True)
    except Exception as e:
        print(e)