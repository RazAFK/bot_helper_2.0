import telebot, time, threading
from settings.TOKEN import *
from db import *
from schedule_funcs import *


sbot = telebot.TeleBot(student_token)

@sbot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id, 'Raz', 'Raz', 10)
    add_theme(message.chat.id, 1, 'smth')
    scheduler_thread = threading.Thread(target=run_scheduler(sbot, 2, 5))
    scheduler_thread.daemon = True
    scheduler_thread.start()
    sbot.send_message(message.chat.id, 'Schedule running')

@sbot.message_handler(content_types=['text'])
def message_receiver(message):
    write_message(message, 2, 1, 0)





if __name__ == "__main__":
    #try:
    sbot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)