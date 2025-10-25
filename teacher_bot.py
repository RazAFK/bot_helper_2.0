import telebot, time, threading
from settings.TOKEN import *
from db import *
from schedule_funcs import *
import settings.settings as sett


tbot = sett.tbot

scheduler_thread = threading.Thread(target=run_scheduler(sbot, 2, scheduled_teacher_task))
scheduler_thread.daemon = True
scheduler_thread.start()


@tbot.message_handler(commands=['start'])
def start(message):
    tbot.send_message(message.chat.id, 'Schedule running')

@tbot.message_handler(content_types=['text'])
def message_receiver(message):
    theme = select_smth(Theme, (Theme.u_id==message.chat.id) & (Theme.status==1))[0]
    write_message(message, theme.id, 2, 1, 0)
    print('new message')





if __name__ == "__main__":
    #try:
    tbot.polling(none_stop=True)
    #except Exception as e:
    #    print(e)