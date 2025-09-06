import telebot, time
from settings.TOKEN import *
from db import *


tbot = telebot.TeleBot(teacher_token)



@tbot.message_handler(commands=['stop']) 
def stop(message):
    if message.chat.id == 1634714523:
        tbot.send_message(message.chat.id, 'Остановка')
        tbot.stop_bot()
        exit()
    else:
        tbot.send_message(message.chat.id, 'Недостаточно полномочий')


@tbot.message_handler(commands=['start'])
def start(message):
    tbot.send_message(message.chat.id, 'Hey')





if __name__ == "__main__":
    try:
        tbot.polling(none_stop=True)
    except Exception as e:
        print(e)