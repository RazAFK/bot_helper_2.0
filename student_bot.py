import telebot, time
from settings.TOKEN import *
from db import *


sbot = telebot.TeleBot(student_token)


@sbot.message_handler(commands=['stop']) 
def stop(message):
    if message.chat.id == 1634714523:
        sbot.send_message(message.chat.id, 'Остановка')
        sbot.stop_bot()
        exit()
    else:
        sbot.send_message(message.chat.id, 'Недостаточно полномочий')


@sbot.message_handler(commands=['start'])
def start(message):
    sbot.send_message(message.chat.id, 'Hey')





if __name__ == "__main__":
    try:
        sbot.polling(none_stop=True)
    except Exception as e:
        print(e)