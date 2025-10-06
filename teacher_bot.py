import telebot, time, threading
from settings.TOKEN import *
from db import *
from schedule_funcs import *


tbot = telebot.TeleBot(teacher_token)

scheduler_thread = threading.Thread(target=run_scheduler(tbot, 2, 5))
scheduler_thread.daemon = True
scheduler_thread.start()


@tbot.message_handler(commands=['start'])
def start(message):
    tbot.send_message(message.chat.id, 'Schedule running')

@tbot.message_handler(content_types=['text'])
def message_receiver(message):
    write_message(message, 2, 1, 0)





if __name__ == "__main__":
    #try:
    tbot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)